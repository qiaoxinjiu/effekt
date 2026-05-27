# encoding: UTF-8
import json
import time
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from const import JENKINS_BASE_URL, JENKINS_USER, JENKINS_TOKEN
from logger import logger
from app.api.model.automationModel import AutoExecution, AutoExecutionCase


class JenkinsPollService(object):
    STATUS_QUEUED = 2
    STATUS_RUNNING = 3
    STATUS_SUCCESS = 4
    STATUS_FAILED = 5

    @staticmethod
    def poll_jenkins_build_status(session, execution_id):
        execution = session.query(AutoExecution).filter(AutoExecution.id == int(execution_id)).first()
        if not execution:
            logger.error(f'执行记录不存在: execution_id={execution_id}')
            return False, '执行记录不存在'
        
        if execution.status not in [JenkinsPollService.STATUS_QUEUED, JenkinsPollService.STATUS_RUNNING]:
            logger.info(f'执行状态不需要轮询: execution_id={execution_id}, status={execution.status}')
            return True, ''
        
        base_url = JENKINS_BASE_URL.rstrip('/')
        job_name = execution.jenkins_job_name
        build_number = execution.jenkins_build_number
        
        if not job_name:
            if execution.jenkins_build_url:
                import re
                match = re.search(r'/job/([^/]+(?:/job/[^/]+)*)/\d+/', execution.jenkins_build_url)
                if match:
                    job_name = match.group(1).replace('/job/', '/')
                    logger.info(f'从构建URL中提取job_name: {job_name}')
                else:
                    logger.error(f'无法从构建URL中提取job_name: {execution.jenkins_build_url}')
                    return False, 'Jenkins job 名称为空'
            else:
                logger.error(f'Jenkins job 名称为空: execution_id={execution_id}')
                return False, 'Jenkins job 名称为空'
        
        auth = HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN) if JENKINS_USER and JENKINS_TOKEN else None
        
        try:
            if not build_number:
                if execution.jenkins_build_url:
                    import re
                    match = re.search(r'/job/([^/]+(?:/job/[^/]+)*)/(\d+)/', execution.jenkins_build_url)
                    if match:
                        job_name = match.group(1).replace('/job/', '/')
                        build_number = match.group(2)
                        logger.info(f'从构建URL中提取: job_name={job_name}, build_number={build_number}')
                    else:
                        logger.error(f'无法从构建URL中提取信息: {execution.jenkins_build_url}')
                
                queue_id = execution.jenkins_queue_id
                if queue_id:
                    queue_url = f'{base_url}/queue/item/{queue_id}/api/json'
                    response = requests.get(queue_url, auth=auth, timeout=30)
                    if response.status_code == 200:
                        queue_data = response.json()
                        logger.debug(f'队列数据: execution_id={execution_id}, queue_data={json.dumps(queue_data, ensure_ascii=False)[:500]}')
                        
                        if queue_data.get('executable'):
                            build_number = queue_data['executable'].get('number')
                            logger.info(f'队列任务已开始执行: execution_id={execution_id}, build_number={build_number}')
                            session.query(AutoExecution).filter(AutoExecution.id == int(execution_id)).update({
                                'jenkins_build_number': build_number,
                                'status': JenkinsPollService.STATUS_RUNNING,
                                'start_time': datetime.now()
                            })
                            session.done(close=False)
                        elif queue_data.get('cancelled') or queue_data.get('blocked'):
                            logger.error(f'队列任务已取消或阻塞: execution_id={execution_id}, cancelled={queue_data.get("cancelled")}, blocked={queue_data.get("blocked")}')
                            end_time = datetime.now()
                            session.query(AutoExecution).filter(AutoExecution.id == int(execution_id)).update({
                                'status': JenkinsPollService.STATUS_FAILED,
                                'end_time': end_time,
                                'trigger_message': queue_data.get('why', '队列任务已取消或阻塞')
                            })
                            session.done(close=False)
                            JenkinsPollService.refresh_execution_summary(session, execution_id, force_finish=True)
                            if execution.plan_id:
                                JenkinsPollService.refresh_plan_status(session, execution.plan_id)
                            return True, '队列任务已取消或阻塞'
                        elif queue_data.get('why'):
                            logger.info(f'队列任务等待中: execution_id={execution_id}, reason={queue_data.get("why")}')
                            return True, f'队列等待中: {queue_data.get("why")}'
                        else:
                            logger.info(f'队列任务等待中: execution_id={execution_id}, queue_id={queue_id}')
                            return True, '队列等待中'
                    else:
                        logger.warning(f'获取队列状态失败: execution_id={execution_id}, status_code={response.status_code}')
                    
                    if response.status_code == 404:
                        logger.info(f'队列项已不存在，尝试查询执行状态: execution_id={execution_id}')
                        builds_url = f'{base_url}/job/{job_name}/builds/api/json?limit=10'
                        try:
                            builds_response = requests.get(builds_url, auth=auth, timeout=30)
                            logger.info(f'构建历史查询: url={builds_url}, status_code={builds_response.status_code}')
                            
                            if builds_response.status_code == 200:
                                builds_data = builds_response.json()
                                logger.info(f'构建历史数据: count={len(builds_data) if builds_data else 0}')
                                
                                if builds_data:
                                    latest_build = builds_data[0]
                                    build_number = latest_build.get('number')
                                    is_building = latest_build.get('building', False)
                                    result = latest_build.get('result')
                                    timestamp = latest_build.get('timestamp', 0)
                                    
                                    logger.info(f'最新构建信息: build_number={build_number}, is_building={is_building}, result={result}')
                                    
                                    if is_building:
                                        status = JenkinsPollService.STATUS_RUNNING
                                    elif result == 'SUCCESS':
                                        status = JenkinsPollService.STATUS_SUCCESS
                                    else:
                                        status = JenkinsPollService.STATUS_FAILED
                                    
                                    logger.info(f'更新执行状态: execution_id={execution_id}, build_number={build_number}, status={status}')
                                    update_info = {
                                        'jenkins_build_number': build_number,
                                        'status': status,
                                        'start_time': datetime.fromtimestamp(timestamp/1000) if timestamp else datetime.now()
                                    }
                                    
                                    if not is_building and result:
                                        update_info['end_time'] = datetime.now()
                                        update_info['jenkins_build_url'] = f'{base_url}/job/{job_name}/{build_number}/'
                                        update_info['console_url'] = f'{base_url}/job/{job_name}/{build_number}/console'
                                        update_info['report_url'] = f'{base_url}/job/{job_name}/{build_number}/allure/'
                                        
                                    session.query(AutoExecution).filter(AutoExecution.id == int(execution_id)).update(update_info)
                                    session.done(close=False)
                                    
                                    if not is_building:
                                        JenkinsPollService.refresh_execution_summary(session, execution_id, force_finish=True)
                                        if execution.plan_id:
                                            JenkinsPollService.refresh_plan_status(session, execution.plan_id)
                                        
                                    return True, f'队列不存在，使用最新构建: {build_number}'
                            else:
                                logger.error(f'获取构建历史失败: status_code={builds_response.status_code}, body={builds_response.text[:200]}')
                        except Exception as err:
                            logger.error(f'查询构建历史异常: {err}')
                    
                    return True, '获取队列状态失败'
                else:
                    logger.warning(f'缺少 queue_id 和 build_number: execution_id={execution_id}')
                    return False, '无法轮询，缺少构建信息'
            
            if build_number:
                build_url = f'{base_url}/job/{job_name}/{build_number}/api/json'
                response = requests.get(build_url, auth=auth, timeout=30)
                if response.status_code == 200:
                    build_data = response.json()
                    is_running = build_data.get('building', False)
                    result = build_data.get('result')
                    
                    console_url = f'{base_url}/job/{job_name}/{build_number}/console'
                    build_url_full = f'{base_url}/job/{job_name}/{build_number}/'
                    
                    if is_running:
                        logger.info(f'构建执行中: execution_id={execution_id}, build_number={build_number}')
                        session.query(AutoExecution).filter(AutoExecution.id == int(execution_id)).update({
                            'status': JenkinsPollService.STATUS_RUNNING,
                            'jenkins_build_url': build_url_full,
                            'console_url': console_url
                        })
                        session.done(close=False)
                        return True, '执行中'
                    else:
                        logger.info(f'构建完成: execution_id={execution_id}, result={result}')
                        end_time = datetime.now()
                        report_url = f'{base_url}/job/{job_name}/{build_number}/allure/'
                        update_info = {
                            'status': JenkinsPollService.STATUS_SUCCESS if result == 'SUCCESS' else JenkinsPollService.STATUS_FAILED,
                            'jenkins_build_url': build_url_full,
                            'console_url': console_url,
                            'report_url': report_url,
                            'end_time': end_time
                        }
                        if execution.start_time:
                            update_info['duration_seconds'] = int((end_time - execution.start_time).total_seconds())
                        session.query(AutoExecution).filter(AutoExecution.id == int(execution_id)).update(update_info)
                        session.done(close=False)
                        
                        JenkinsPollService.refresh_execution_summary(session, execution_id, force_finish=True)
                        if execution.plan_id:
                            JenkinsPollService.refresh_plan_status(session, execution.plan_id)
                        
                        return True, f'构建完成: {result}'
            
        except Exception as err:
            logger.error(f'轮询 Jenkins 状态失败: execution_id={execution_id}, error={err}')
            return False, str(err)
        
        return True, ''

    @staticmethod
    def refresh_execution_summary(session, execution_id, force_finish=False):
        from sqlalchemy import func
        
        rows = session.query(AutoExecutionCase.status, func.count(AutoExecutionCase.id)).filter(
            AutoExecutionCase.execution_id == int(execution_id)
        ).group_by(AutoExecutionCase.status).all()
        
        summary = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
        for status, count in rows:
            summary[int(status)] = int(count)
        total = sum(summary.values())
        
        execution = session.query(AutoExecution).filter(AutoExecution.id == int(execution_id)).first()
        if execution:
            update_info = {
                'total_count': total,
                'pending_count': summary.get(0, 0),
                'running_count': summary.get(1, 0),
                'passed_count': summary.get(2, 0),
                'failed_count': summary.get(3, 0),
                'blocked_count': summary.get(4, 0),
                'skipped_count': summary.get(5, 0),
                'not_found_count': summary.get(6, 0)
            }
            
            running_count = summary.get(1, 0)
            finished_count = summary.get(2, 0) + summary.get(3, 0) + summary.get(4, 0) + summary.get(5, 0) + summary.get(6, 0) + summary.get(7, 0)
            
            if running_count > 0:
                update_info['status'] = JenkinsPollService.STATUS_RUNNING
            elif total > 0 and finished_count == total:
                if summary.get(3, 0) + summary.get(4, 0) + summary.get(6, 0) > 0:
                    update_info['status'] = JenkinsPollService.STATUS_FAILED
                else:
                    update_info['status'] = JenkinsPollService.STATUS_SUCCESS
            
            if force_finish or (total > 0 and finished_count == total):
                end_time = execution.end_time or datetime.now()
                update_info['end_time'] = end_time
                if execution.start_time:
                    update_info['duration_seconds'] = int((end_time - execution.start_time).total_seconds())
            
            session.query(AutoExecution).filter(AutoExecution.id == int(execution_id)).update(update_info)
            session.done(close=False)

    @staticmethod
    def refresh_plan_status(session, plan_id):
        from sqlalchemy import func
        
        rows = session.query(
            AutoExecution.status, func.count(AutoExecution.id)
        ).filter(
            AutoExecution.plan_id == int(plan_id),
            AutoExecution.status.in_([JenkinsPollService.STATUS_RUNNING, JenkinsPollService.STATUS_SUCCESS, JenkinsPollService.STATUS_FAILED])
        ).group_by(AutoExecution.status).all()
        
        status_counts = {}
        for status, count in rows:
            status_counts[status] = count
        
        running_count = status_counts.get(JenkinsPollService.STATUS_RUNNING, 0)
        success_count = status_counts.get(JenkinsPollService.STATUS_SUCCESS, 0)
        failed_count = status_counts.get(JenkinsPollService.STATUS_FAILED, 0)
        
        from app.api.model.planModel import TestPlan
        
        if running_count > 0:
            session.query(TestPlan).filter(TestPlan.id == int(plan_id)).update({'status': 1})
        elif success_count > 0 and failed_count == 0:
            session.query(TestPlan).filter(TestPlan.id == int(plan_id)).update({'status': 4})
        elif success_count + failed_count > 0:
            session.query(TestPlan).filter(TestPlan.id == int(plan_id)).update({'status': 2})
        
        session.done(close=False)

    @staticmethod
    def poll_all_pending_executions(session):
        pending_executions = session.query(AutoExecution).filter(
            AutoExecution.status.in_([JenkinsPollService.STATUS_QUEUED, JenkinsPollService.STATUS_RUNNING])
        ).all()
        
        for execution in pending_executions:
            try:
                success, msg = JenkinsPollService.poll_jenkins_build_status(session, execution.id)
                logger.info(f'轮询执行 {execution.id}: success={success}, msg={msg}')
            except Exception as err:
                logger.error(f'轮询执行 {execution.id} 异常: {err}')
        
        session.done(close=False)
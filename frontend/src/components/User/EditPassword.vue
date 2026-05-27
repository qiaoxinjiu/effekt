<template>
    <div class="password-edit">
      <div class="username">
        <span>学生证号：{{username}}</span>
      </div>
      <div class="password">
        <span>新密码：</span>
        <el-input v-model="password"></el-input>
        <el-button type="primary" @click.native.prevent="confirmPassword">确定</el-button>
      </div>
    </div>
</template>

<script>
  import {editPassword} from '@/api/Userapi'
    export default {
        name: "EditPassword",
      props: ['username','userid'],
      data(){
          return {
            password:''
          }
        },
      methods:{
        confirmPassword(){
            if(this.password!==undefined &&this.password!==''){
              let data = {userId:this.userid,new_password:this.password,sure_password:this.password};
              editPassword(data).then(data=>{
                if(data.code===200){
                  this.password='';
                  this.$message({
                    type: 'success',
                    message: data.message
                  });
                }else {
                  this.$message({
                    type: 'error',
                    message:data.message
                  });
                }
              })
            }else {
              this.$message({
                type: 'info',
                message: "请输入密码"
              });
            }
          }
      }
    }
</script>

<style scoped>
  .el-input{
    width: 200px;
  }
  .username{
    padding-bottom: 20px;
  }
</style>

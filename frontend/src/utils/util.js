export function formatTime(str) {
  if (str.length === 8) {
    return str.toString().substring(0, 4) + '-' + str.toString().substring(4, 6) + '-' + str.toString().substring(6, 8)
  }
  return str.toString().substring(0, 4) + '-' + str.toString().substring(4, 6) + '-' + str.toString().substring(6, 8) + ' ' + str.toString().substring(8, 10) + ':' + str.toString().substring(10, 12)
}

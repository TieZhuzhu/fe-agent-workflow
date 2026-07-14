/**
 * HiTable（Vue 2）内置列表请求，复制组件目录时一并复制
 * 按项目 request 工具调整 import 路径与调用方式
 */
import request from '@/config/request'

export function listRequest(url, data, method = 'post') {
  return request({ url, data, method })
}

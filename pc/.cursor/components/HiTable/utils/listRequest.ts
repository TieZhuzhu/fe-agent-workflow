/**
 * HiTable 内置列表请求，复制组件目录时一并复制
 * 按项目 request 工具调整 import 路径与调用方式
 */
import request from '@/config/request'

interface ListResponse {
  data?: {
    data?: unknown[]
    total?: number
  }
}

export function listRequest(
  url: string,
  data: Record<string, unknown>,
  method = 'post'
): Promise<ListResponse> {
  return request({ url, data, method })
}

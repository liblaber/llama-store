package hooks

import (
	"fmt"
)

type CustomHook struct{}

func NewCustomHook() Hook {
	return &CustomHook{}
}

func (h *CustomHook) BeforeRequest(req Request) Request {
	fmt.Printf("Before request on URL %#v with method %#v\n", req.GetBaseUrl(), req.GetMethod())
	return req
}

func (h *CustomHook) AfterResponse(req Request, resp Response) Response {
	fmt.Printf("After response on URL %#v with method %#v, returning status %d\n", req.GetBaseUrl(), req.GetMethod(), resp.GetStatusCode())
	return resp
}

func (h *CustomHook) OnError(req Request, resp ErrorResponse) ErrorResponse {
	fmt.Printf("On Error: %#v\n", resp.Error())
	return resp
}

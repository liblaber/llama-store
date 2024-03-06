
public class CustomHook : IHook
{
  public async Task<HttpRequestMessage> BeforeRequestAsync(HttpRequestMessage request)
  {
    Console.WriteLine($"Before request on URL {request.RequestUri.AbsoluteUri} with method {request.Method.ToUpper()}");
    return request;
  }

  public async Task<HttpResponseMessage> AfterResponseAsync(HttpResponseMessage response)
  {
    Console.WriteLine($"After response on URL {response.RequestMessage.RequestUri.AbsoluteUri} with method {response.RequestMessage.Method.ToUpper()}, returning status {response.StatusCode}")
    return response;
  }

  public async Task OnErrorAsync(HttpResponseMessage response)
  {
    Console.WriteLine($"On error - {response.StatusCode} - {response.ReasonPhrase}");
  }
}

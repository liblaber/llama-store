#pragma warning disable 1998 // This async method lacks 'await' operators
#pragma warning disable 8603 // Possible null reference return.

public class CustomHook : IHook
{
  public async Task<HttpRequestMessage> BeforeRequestAsync(HttpRequestMessage request)
  {
    Console.WriteLine($"Before request on URL {request?.RequestUri?.AbsoluteUri} with method {request?.Method.ToString().ToUpper()}");
    return request;
  }

  public async Task<HttpResponseMessage> AfterResponseAsync(HttpResponseMessage response)
  {
    Console.WriteLine($"After response on URL {response?.RequestMessage?.RequestUri?.AbsoluteUri} with method {response?.RequestMessage?.Method.ToString().ToUpper()}, returning status {response?.StatusCode}");
    return response;
  }

  public async Task OnErrorAsync(HttpResponseMessage response)
  {
    Console.WriteLine($"On error - {response?.StatusCode} - {response?.ReasonPhrase}");
  }
}

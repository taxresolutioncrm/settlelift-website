export async function onRequest(context) {
  const response = await context.next();
  const result = new Response(response.body, response);
  const host = new URL(context.request.url).hostname;
  if (host !== "settlelift.com" && host !== "www.settlelift.com") {
    result.headers.set("X-Robots-Tag", "noindex, nofollow");
  } else {
    result.headers.delete("X-Robots-Tag");
  }
  return result;
}



<!-- bazel run //:migrate -- revision --autogenerate -m "add email" -->
bazelisk run //:migrate -- revision  -m "add email"
bazelisk run //:migrate -- upgrade head

# Windows PowerShell 用：
$env:HTTP_PROXY="http://127.0.0.1:10809"
$env:HTTPS_PROXY="http://127.0.0.1:10809"




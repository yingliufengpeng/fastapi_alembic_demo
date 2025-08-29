

<!-- bazel run //:migrate -- revision --autogenerate -m "add email" -->
bazel run //:migrate -- revision  -m "add email"
bazel run //:migrate -- upgrade head



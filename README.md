

<!-- bazel run //:migrate -- revision --autogenerate -m "add email" -->
bazelisk run //:migrate -- revision  -m "add email"
bazelisk run //:migrate -- upgrade head



lib: python_pkgs:
lib.buildPythonPackage rec {
  pname = "mypy-boto3-redshift";
  version = "1.28.64";
  src = lib.fetchPypi {
    inherit pname version;
    sha256 = "Drl6RTntuwVOW+9mxBWOJNktG/83mX0twhhYa+SwtGs=";
  };
  nativeBuildInputs = with python_pkgs; [boto3];
  propagatedBuildInputs = with python_pkgs; [botocore typing-extensions];
}

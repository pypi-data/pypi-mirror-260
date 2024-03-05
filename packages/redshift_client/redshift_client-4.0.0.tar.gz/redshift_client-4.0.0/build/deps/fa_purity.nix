{
  lib,
  makesLib,
  nixpkgs,
  python_pkgs,
  python_version,
}: let
  raw_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    rev = "7b13ef0b00cb0985561c625534894275f120b4b7";
    ref = "refs/tags/v1.42.0";
  };
  src = import "${raw_src}/build/filter.nix" nixpkgs.nix-filter raw_src;
  bundle = import "${raw_src}/build" {
    inherit makesLib nixpkgs python_version src;
  };
in
  bundle.build_bundle (
    default: required_deps: builder:
      builder lib (
        required_deps (
          python_pkgs
          // {
            inherit (default.python_pkgs) types-simplejson;
          }
        )
      )
  )

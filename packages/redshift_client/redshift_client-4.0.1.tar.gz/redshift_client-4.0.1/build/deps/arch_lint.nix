{
  lib,
  makesLib,
  nixpkgs,
  python_pkgs,
  python_version,
}: let
  raw_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/arch_lint";
    rev = "fd64a300bda15c2389f5bfb314f48fb5b2a0e47a";
    ref = "refs/tags/2.4.0+2";
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
            inherit (default.python_pkgs) grimp;
          }
        )
      )
  )

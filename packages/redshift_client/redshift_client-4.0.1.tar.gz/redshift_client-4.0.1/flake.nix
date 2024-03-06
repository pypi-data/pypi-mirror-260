{
  description = "Redshift client-SDK";
  inputs = {
    makes.url = "github:fluidattacks/makes";
    nixpkgs.url = "github:nixos/nixpkgs";
    nix_filter.url = "github:numtide/nix-filter";
  };
  outputs = {
    self,
    makes,
    nixpkgs,
    nix_filter,
  }: let
    path_filter = nix_filter.outputs.lib;
    src = import ./build/filter.nix path_filter self;
    out = system: python_version: let
      makesLib = makes.lib."${system}";
      pkgs = nixpkgs.legacyPackages."${system}";
    in
      import ./build {
        inherit makesLib python_version src;
        nixpkgs = pkgs // {nix-filter = path_filter;};
      };
    supported = ["python39" "python310" "python311"];
    python_outs = system:
      (builtins.listToAttrs (map (name: {
          inherit name;
          value = out system name;
        })
        supported))
      // {build_with_python = out system;};
    systems = [
      "aarch64-darwin"
      "aarch64-linux"
      "x86_64-darwin"
      "x86_64-linux"
    ];
    forAllSystems = nixpkgs.lib.genAttrs systems;
  in {
    packages = forAllSystems python_outs;
    defaultPackage = self.packages;
  };
}

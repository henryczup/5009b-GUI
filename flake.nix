{
  # Flake inputs
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  # Flake outputs
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        v5009cm = (with pkgs;
          python3Packages.buildPythonPackage rec {
            pname = "v5009cm";
            version = "1.0";

            src = nix-gitignore.gitignoreSource [ "*.nix" ] ./.;

            propagatedBuildInputs = with python3Packages; [ pyserial tkinter ];

            doCheck = false;
          });

      in
      {
        packages.default = v5009cm;

        devShells.default = pkgs.mkShell {
          # Packages
          packages = (with pkgs; [
            (python3.withPackages (ps: [
              v5009cm
              ps.autopep8
              ps.flake8
            ]))
          ]);
        };
      }
    );
}

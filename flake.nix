{
  description = "Zero shot term typing using LLMs";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.systems.url = "github:nix-systems/default";
  inputs.flake-utils = {
    url = "github:numtide/flake-utils";
    inputs.systems.follows = "systems";
  };

  outputs =
    { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python312;

        # GitHub-based python packages
        ontospy = pkgs.python3Packages.buildPythonPackage rec {
          name = "Ontospy";
          version = "v2.1.1";

          src = pkgs.fetchFromGitHub {
            owner = "lambdamusic";
            repo = "${name}";
            rev = "${version}";
            hash = "sha256-1vbmzj2x67hfm8al1sqzkl98f9vmf8nn0z9zcvnzgd9vavh22lhs=";
          };

        };

        # Build Packages
        pythonBuildPackages = (
          python.withPackages (
            ps: with ps; [
              setuptools
            ]
          )
        );

        # Python modules for actual package
        modulePythonPackages = (
          python.withPackages (
            ps: with ps; [
              ontospy
              openai
              polars
              pydantic
              python-dotenv
              scikit-learn
              torch
              tqdm
              transformers
            ]
          )
        );

        # Python development packages used for development
        # LSP, formatting, etc.
        devPythonPackages = (
          python.withPackages (
            ps: with ps; [
              python-lsp-server
              isort
              black
              flake8
            ]
          )
        );

        # Other development packages available in the nixpkgs
        devPackages = (
          with pkgs;
          [
            nixd
            nixfmt-rfc-style
          ]
        );

        # The main module
        myapp = pkgs.python3Packages.buildPythonPackage rec {
          # Change name here
          pname = "llm_zero_shot_term_typing_impact";
          pyproject = true;
          version = "1.0.0";
          src = ./.;
          build-system = [
            pythonBuildPackages
            modulePythonPackages
          ];
        };

      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.bashInteractive
            devPythonPackages
            modulePythonPackages
            devPackages
            myapp
          ];
        };
      }
    );
}

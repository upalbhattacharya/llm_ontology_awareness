let
  # We pin to a specific nixpkgs commit for reproducibility.
  # Last updated: 2024-04-29. Check for new commits at https://status.nixos.org.
  pkgs = import <nixpkgs> { };
  python = pkgs.python311;
in pkgs.mkShell {
  packages = [
    (python.withPackages (python-pkgs:
      with python-pkgs; [
        openai
        polars
        pydantic
        python-dotenv
        scikit-learn
        torch
        tqdm
        transformers
        black
        isort
        python-lsp-server
        flake8
      ]))
  ];
}

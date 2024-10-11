let
  pkgs = import <nixpkgs> { };
  python = pkgs.python312;
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
    # nix-based
    pkgs.nixd
    pkgs.nixfmt-rfc-style
  ];
}

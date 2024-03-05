# Komodo Package

This is Komodo SDK package.

## Package hierarchy

- komodo/server: Flask / FastApi server for the Komodo Appliances
- komodo/models: Implementation of LLM model access and runners to get responses.
-
- komodo/loaders: Loaders for komodo classes and objects.
- komodo/core: Implementation of komodo agents, tools, data sources and other core components.
- komodo/shared: Shared utilities and classes used by other komodo packages.

- komodo/framework: KomodoApp, KomodoAgents that form the Komodo AI platform.
- komodo/store: Ability to store and load proto objects from redis database.
- komodo/proto: Protobuf files that define the basic data structures and services.

## Pushing to PyPi

```bash
python3 -m build
python3 -m twine upload dist/*
```

## Pushing website image to AWS ECR

This should happen using github actions but failing on permissions currently.

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/k9s5f5s5
docker build -t website .
docker tag website:latest public.ecr.aws/k9s5f5s5/website:latest
docker push public.ecr.aws/k9s5f5s5/website:latest
```


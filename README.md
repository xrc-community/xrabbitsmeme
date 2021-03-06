# XRC MEME

## Install
1. Install [poetry](https://python-poetry.org/)
2. Setup virtual env. I suggest to use `pyenv` & `virtualenv`.
3. Install dependence
```bash
poetry install
```
4. Install postgresql
```bash
brew install postgresql
brew services restart postgresql
```
5. Create database. `xrc` below is the db name.
```bash
createdb xrc
# after createdb, enter the xrc db
psql -d xrc
```
6. Create `.env` file in root path
```bash
DB_HOST=localhost
DB_USER=your postgresql user for xrc
DB_DATABASE=xrc
```
7. Upgrade db
```bash
poetry run alembic upgrade head
```
8. Run the server
```bash
poetry run uvicorn xrabbitsmeme.asgi:app --reload
```

9. Run worker
```bash
poetry run arq xrabbitsmeme.worker.WorkerSettings
```

10. Make migration
```bash
poetry run alembic revision --autogenerate -m 'message here' 
```

Now you can visit `http://localhost:8000/docs` to see docs.

## Cli
### Create NFT, Download NFT info and image 
```bash
python src/xrabbitsmeme/cli/nft.py create-nfts 'QmShUrXkgxjQ1eeCuo7hywsK42cGYj6KQ8N5XomM7d9A9M'
```

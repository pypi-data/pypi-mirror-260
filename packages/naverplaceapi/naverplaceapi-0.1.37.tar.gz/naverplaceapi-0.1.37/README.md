
# Naverplace 데이터 수집 API

# History
## 2024.02.03
- 블로그, 리뷰 수집기능 추가



# Update
```bash
pip install --upgrade naverplaceapi
```


# Build and publish
```bash
poetry build  # Bui[place.py](naverplaceapi%2Fmixin%2Fplace.py)ld
python -m twine upload --skip-existing dist/*   # Deployment
```
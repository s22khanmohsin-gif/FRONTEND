# Model Validation Testing - How to Use

## Quick Start

### 1. Test Model Directly (Offline)
Run the comprehensive model validation script:

```bash
python test_model.py
```

This will:
- ✓ Run sanity checks
- ✓ Test predictions with 7 different scenarios
- ✓ Display feature importance (if available)
- ✓ Show color-coded results

**Requirements:** `pip install colorama`

---

### 2. Test Flask API (Online)
First, start your Flask app:
```bash
python app.py
```

Then in another terminal, run the API tests:
```bash
python test_api.py
```

This will:
- ✓ Test the `/predict` endpoint with 5 scenarios
- ✓ Validate API responses
- ✓ Check if predictions match expected risk levels

**Requirements:** `pip install requests colorama`

---

### 3. Automated Test Endpoint
Visit in your browser or use curl:
```bash
curl http://localhost:7860/test
```

This returns JSON with:
- Test results for 3 predefined scenarios
- Pass/fail status for each
- Overall summary

Perfect for automated health checks!

---

## Test Scripts Overview

| Script | Purpose | Requires Server |
|--------|---------|----------------|
| `test_model.py` | Direct model testing | ❌ No |
| `test_api.py` | API endpoint testing | ✅ Yes |
| `/test` endpoint | Automated validation | ✅ Yes |

---

## Expected Output

### ✅ Successful Test
```
🎉 ALL TESTS PASSED! Model is working correctly.
```

### ❌ Failed Test
```
⚠ SOME TESTS FAILED. Please review the output above.
```

Each test shows:
- 🟢 Green = Low risk / Passed
- 🟡 Yellow = Medium risk
- 🔴 Red = High risk / Failed

---

## Troubleshooting

**"Model file not found"**
- Ensure `model_fixed.pkl` is in the Frontend directory

**"Cannot connect to API"**
- Start Flask app: `python app.py`
- Check it's running on port 7860

**"ModuleNotFoundError: colorama"**
- Install: `pip install colorama`

---

## What Each Test Validates

### Sanity Checks
1. Model accepts 9-feature input
2. Probabilities sum to 1.0
3. Output is binary (0 or 1)
4. Feature count matches

### Prediction Tests
- High risk profiles → Should predict >50% probability
- Low risk profiles → Should predict <40% probability
- Medium risk → Between 30-70%
- Edge cases with min/max values

### Feature Importance
Shows which features the model considers most important for predictions

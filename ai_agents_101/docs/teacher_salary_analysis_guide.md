# Teacher Salary Analysis - Optimal Prompt & Validation Guide

## Meta-Analysis: How to Get This Right From the Start

This document captures the lessons learned from a complex teacher salary analysis project, including the optimal prompt, expected results for validation, and key pitfalls to avoid.

---

## 🎯 The Optimal Prompt

Use this prompt to get accurate, defensible results from the beginning:

```
Pull teacher salary data from the US Census Bureau ACS 5-year survey
for county-level data across three states (you pick). Use the most
recent available year and DOCUMENT which year you're using.

Then:
1. Clean data and focus on RELIABLE estimates:
   - Filter to larger counties (population > 50,000)
   - Remove counties with missing or unreliable salary data
   - Document how many counties you started with vs. final dataset

2. Calculate cost-of-living adjustments using a DEFENSIBLE methodology:
   - Housing should be weighted at 30-40% of total expenses (not 100%!)
   - Other costs (food, gas, healthcare) vary less regionally
   - Formula: COL_adjustment_factor = 1 / (1 + housing_premium * 0.33)
   - Explain your methodology in detail and why it's reasonable
   - Compare to alternatives (BEA Regional Price Parities if possible)

3. Feature engineering: Include both raw economic features AND
   housing affordability metrics:
   - Median household income, per capita income
   - Education levels (% with bachelor's degree)
   - Population, poverty rate, unemployment rate
   - Home value-to-salary ratio, rent-to-salary ratio
   - Housing cost ratios relative to national median

4. Build a Random Forest model to predict COL-ADJUSTED teacher salaries:
   - Use 80/20 train-test split
   - Report both training and test metrics
   - Extract and rank feature importances

5. Throughout the analysis, VALIDATE YOUR RESULTS:
   - Sanity check: Do adjusted salaries make sense? (should be > $20k)
   - Compare raw vs adjusted salaries side-by-side
   - Show example calculations for 3 counties (high/medium/low COL)
   - If something looks fishy (e.g., "teachers earning minimum wage"),
     STOP and reconsider your approach
   - Ask: "Does this match real-world intuition?"

6. Report:
   - State-level summary statistics (raw and COL-adjusted)
   - Feature importance rankings
   - R² and MAE for the model
   - Top 10 and bottom 10 counties by:
     a) COL-adjusted salary (purchasing power)
     b) Predicted vs actual gap (model residuals)
   - Clear explanation of what drives teacher salary differences

7. Create visualizations that show:
   - Model performance (predicted vs actual)
   - Impact of COL adjustment (before/after scatter plot)
   - State-level differences (distributions)
   - COL index by state
   - Housing affordability for teachers
   - Prediction error distribution

8. Save results:
   - Comprehensive CSV with all features and predictions
   - High-quality visualization (300 DPI, multi-panel)
   - Summary statistics table
```

---

## 📅 Expected Results (ACS 2021 5-Year Data)

**IMPORTANT:** Results are specific to ACS 2021 5-Year Survey. Different years will have different values.

### Dataset Characteristics

**Starting Point:**
- Total counties across CA, TX, NY: 374
- After filtering (population > 50k): 154 counties
- Data source: Table S2411_C01_013E (Educational instruction and library occupations)

**Data Quality Notes:**
- This variable includes K-12 teachers, college professors, and librarians (not purely K-12)
- Better alternative: PUMS microdata with specific occupation codes (requires bulk download)
- Small counties have unreliable estimates due to small sample sizes

### State-Level Summary (2021 Data)

#### Raw Salaries (Before COL Adjustment)
| State      | Counties | Avg Salary | Median Salary | Std Dev |
|------------|----------|------------|---------------|---------|
| California | 43       | $45,260    | $46,673       | $6,794  |
| Texas      | 66       | $47,606    | $47,838       | $5,544  |
| New York   | 45       | $51,626    | $50,779       | $7,903  |

#### COL-Adjusted Salaries (Proper Method: Housing = 33%)
| State      | Avg COL-Adj | Change from Raw | COL Index |
|------------|-------------|-----------------|-----------|
| California | $35,009     | -22.6%          | 133       |
| Texas      | $49,718     | +4.4%           | 96        |
| New York   | $51,099     | -1.0%           | 103       |

**Key Insight:** California teachers lose ~23% purchasing power due to housing costs. Texas teachers gain ~4% due to lower housing costs. New York is roughly neutral.

### Top 10 Counties by COL-Adjusted Salary (2021)

| Rank | County                    | State | Raw Salary | COL-Adj Salary | Change  |
|------|---------------------------|-------|------------|----------------|---------|
| 1    | Fulton County             | NY    | $56,196    | $64,068        | +14.0%  |
| 2    | Ulster County             | NY    | $65,469    | $63,068        | -3.7%   |
| 3    | Steuben County            | NY    | $53,464    | $62,316        | +16.6%  |
| 4    | Oneida County             | NY    | $54,840    | $61,500        | +12.1%  |
| 5    | Webb County               | TX    | $55,167    | $60,854        | +10.3%  |
| 6    | Warren County             | NY    | $59,346    | $60,610        | +2.1%   |
| 7    | Niagara County            | NY    | $53,499    | $60,332        | +12.8%  |
| 8    | Hidalgo County            | TX    | $51,095    | $60,034        | +17.5%  |
| 9    | Dutchess County           | NY    | $65,962    | $59,868        | -9.2%   |
| 10   | Chautauqua County         | NY    | $49,850    | $59,364        | +19.1%  |

**Pattern:** Rural New York and Texas counties dominate the top 10. Low housing costs give teachers better purchasing power.

### Bottom 10 Counties by COL-Adjusted Salary (2021)

| Rank | County                    | State | Raw Salary | COL-Adj Salary | Change  |
|------|---------------------------|-------|------------|----------------|---------|
| 1    | Santa Barbara County      | CA    | $32,138    | $22,170        | -31.0%  |
| 2    | Santa Clara County        | CA    | $47,308    | $23,726        | -49.8%  |
| 3    | Mendocino County          | CA    | $30,928    | $26,070        | -15.7%  |
| 4    | San Francisco County      | CA    | $54,041    | $27,022        | -50.0%  |
| 5    | San Mateo County          | CA    | $56,992    | $27,341        | -52.0%  |
| 6    | Marin County              | CA    | $55,104    | $28,220        | -48.8%  |
| 7    | Los Angeles County        | CA    | $42,493    | $29,298        | -31.1%  |
| 8    | Lake County               | CA    | $30,463    | $29,335        | -3.7%   |
| 9    | Alameda County            | CA    | $50,817    | $29,931        | -41.1%  |
| 10   | Sonoma County             | CA    | $44,787    | $30,025        | -33.0%  |

**Pattern:** California counties, especially Bay Area, dominate the bottom 10. High housing costs crush purchasing power.

### COL Adjustment Examples (2021 Data)

**Example 1: San Mateo County, CA (High COL)**
```
National median home value: $220,250
San Mateo home value: $945,000 (4.29x national)
Housing cost ratio: 4.29
Housing premium: 3.29 (329% more expensive)
COL impact: 3.29 × 0.33 = 1.09 (109% higher COL)
COL adjustment factor: 1 / (1 + 1.09) = 0.48
Raw salary: $56,992
COL-adjusted salary: $56,992 × 0.48 = $27,341 (-52%)
```

**Example 2: Fulton County, NY (Low COL)**
```
Fulton home value: $93,000 (0.42x national)
Housing cost ratio: 0.42
Housing premium: -0.58 (-58% cheaper)
COL impact: -0.58 × 0.33 = -0.19 (-19% lower COL)
COL adjustment factor: 1 / (1 - 0.19) = 1.24
Raw salary: $56,196
COL-adjusted salary: $56,196 × 1.24 = $69,683 (+24%)
```

**Example 3: Harris County, TX (Medium COL)**
```
Harris home value: $202,000 (0.92x national)
Housing cost ratio: 0.92
Housing premium: -0.08 (-8% cheaper)
COL impact: -0.08 × 0.33 = -0.03 (-3% lower COL)
COL adjustment factor: 1 / (1 - 0.03) = 1.03
Raw salary: $53,897
COL-adjusted salary: $53,897 × 1.03 = $55,514 (+3%)
```

### Model Performance (2021 Data)

**Random Forest Metrics:**
- Training R²: 0.9799
- Test R²: 0.8953
- Training MAE: $995
- Test MAE: $2,634

**Validation:** R² of 0.90 is excellent but not suspiciously perfect. MAE of ~$2,600 is reasonable (5-6% error on average).

### Feature Importance Rankings (2021 Data)

| Rank | Feature                        | Importance |
|------|--------------------------------|------------|
| 1    | rent_to_salary_ratio           | 51.1%      |
| 2    | home_value_to_salary_ratio     | 36.4%      |
| 3    | income_to_salary_ratio         | 2.4%       |
| 4    | median_gross_rent              | 1.7%       |
| 5    | poverty_rate                   | 1.6%       |
| 6    | median_household_income        | 1.3%       |
| 7    | median_age                     | 1.1%       |
| 8    | log_population                 | 0.7%       |
| 9    | unemployment_rate              | 0.7%       |
| 10   | wealth_index                   | 0.6%       |

**Key Insight:** Housing affordability dominates (87.5% combined). Other economic factors are secondary.

---

## 🚨 Common Pitfalls & How to Avoid Them

### Pitfall 1: Naive COL Adjustment (Housing = 100% of expenses)

**What Went Wrong:**
- Initial approach: `adjusted_salary = raw_salary × (national_housing / local_housing)`
- This treats housing as 100% of living expenses
- Result: San Mateo teachers appeared to make $18k adjusted (absurd!)

**Why It's Wrong:**
- Housing is ~30-35% of consumer spending (BLS data)
- Food, gas, healthcare, utilities don't vary 5x between regions
- Over-adjusting creates nonsensical results

**Correct Approach:**
```python
# Calculate housing premium
housing_cost_ratio = local_housing / national_housing
housing_premium = housing_cost_ratio - 1.0

# Weight housing at 33% of total expenses
col_impact = housing_premium * 0.33

# Calculate adjustment factor
col_adjustment_factor = 1.0 / (1.0 + col_impact)

# Apply adjustment
adjusted_salary = raw_salary * col_adjustment_factor
```

**Validation:** If housing is 4x more expensive:
- Old method: Salary worth 0.25x (75% loss) ❌
- New method: Salary worth 0.57x (43% loss) ✓

### Pitfall 2: Including Small Counties

**What Went Wrong:**
- Initial dataset included all 374 counties
- Small counties (pop < 10k) have unreliable estimates
- Created outliers: Sierra County, CA showed $76k salary (pop: 3,000)

**Why It's Wrong:**
- ACS estimates have high margins of error for small populations
- Small samples create noise in the model
- Outliers can skew feature importance

**Correct Approach:**
- Filter to counties with population > 50,000
- Document the filter threshold and counties removed
- 374 → 154 counties (improvement in reliability)

### Pitfall 3: Not Validating Results

**What Went Wrong:**
- Accepted results showing teachers earning "$16k adjusted"
- Didn't ask: "Can anyone actually live on this?"
- No sanity checks on outputs

**Why It's Wrong:**
- Models can produce nonsensical results if methodology is flawed
- Garbage in, garbage out
- Need to validate against real-world intuition

**Correct Approach:**
- **Sanity Check 1:** Are all adjusted salaries > $20k? (poverty threshold)
- **Sanity Check 2:** Are adjustments between -60% and +30%? (reasonable range)
- **Sanity Check 3:** Do state averages match perception? (CA expensive, TX cheap)
- **Sanity Check 4:** Show 3 example calculations step-by-step

### Pitfall 4: Not Documenting Methodology

**What Went Wrong:**
- Made up COL adjustment formula without explanation
- Didn't document assumptions or alternatives
- Hard to defend choices

**Correct Approach:**
- Explain the formula with actual numbers
- Cite sources (BLS consumer expenditure data)
- Compare to alternatives (BEA Regional Price Parities)
- Document assumptions and limitations

### Pitfall 5: Data Source Limitations Not Acknowledged

**What Went Wrong:**
- Used S2411_C01_013E without noting it includes professors and librarians
- Didn't mention better alternatives exist (PUMS microdata)
- Claimed "teacher salary" when it's actually "education occupations"

**Correct Approach:**
- Acknowledge data limitations upfront
- Note: "This includes K-12 teachers, college professors, and librarians"
- Suggest better alternatives: "PUMS data with SOC codes 25-2021, 25-2031 would be more accurate but requires bulk download"
- Be honest about trade-offs

---

## ✅ Validation Checklist

Use this checklist to validate your results:

### Data Quality
- [ ] Year documented? (e.g., ACS 2021 5-Year)
- [ ] Source documented? (e.g., Table S2411_C01_013E)
- [ ] Sample size adequate? (counties > 50k population)
- [ ] Missing data handled? (removed or imputed?)
- [ ] Outliers investigated? (especially small counties)

### COL Adjustment
- [ ] Methodology explained with formula?
- [ ] Housing weight documented? (30-40% range)
- [ ] Example calculations shown? (3+ examples)
- [ ] National medians documented? (reference values)
- [ ] Adjustment range reasonable? (-60% to +30%)

### Sanity Checks
- [ ] All adjusted salaries > $20k? (no extreme poverty)
- [ ] State averages match intuition? (CA expensive, TX cheap)
- [ ] Top counties make sense? (rural NY/TX have better purchasing power)
- [ ] Bottom counties make sense? (Bay Area has worst purchasing power)
- [ ] No adjustments > 60% loss? (housing isn't everything)

### Model Quality
- [ ] R² between 0.80-0.95? (good but not perfect)
- [ ] MAE < 10% of mean salary? (reasonable error)
- [ ] Feature importance makes sense? (housing affordability dominant)
- [ ] No data leakage? (didn't include target in features)
- [ ] Train/test split used? (80/20 or 70/30)

### Presentation
- [ ] Visualizations clear and informative?
- [ ] Before/after comparison shown?
- [ ] State-level summary provided?
- [ ] Top/bottom 10 counties listed?
- [ ] Limitations acknowledged?

---

## 📚 Key Lessons Learned

### 1. Specific Prompts Get Better Results

**Vague:** "Adjust for cost of living"
**Specific:** "Calculate COL adjustment with housing weighted at 33% of expenses"

The more specific your methodological constraints, the better the initial results.

### 2. Validation is Critical

Don't blindly accept model outputs. Ask:
- Does this make sense?
- Can I explain this to a skeptical audience?
- Are there obvious red flags?

If teachers appear to earn "minimum wage equivalent," your methodology is broken.

### 3. Document Everything

Future you (or others) will need to understand:
- What year of data?
- What variables exactly?
- What formula for adjustments?
- What assumptions were made?

### 4. Trade-offs Are Real

- **Aggregate tables (S2411):** Easy to access, but less precise
- **PUMS microdata:** More precise, but requires bulk downloads
- **All counties:** More data, but less reliable
- **Large counties only:** Less data, but more reliable

Document the trade-offs you make.

### 5. Comparison Reveals Flaws

Showing raw vs. adjusted salaries side-by-side immediately revealed the flawed methodology. Always include before/after comparisons.

### 6. Domain Knowledge Matters

Need to know:
- Housing is ~33% of consumer spending (BLS data)
- ACS has margins of error for small populations
- Teacher salaries vary by occupation type (K-12 vs. college)
- Cost of living indices exist (BEA RPP, ACCRA)

Don't reinvent the wheel—use established methodologies.

### 7. Iteration is Normal

The path to the correct answer:
1. **V1:** All counties, naive COL adjustment → Nonsensical results
2. **V2:** Large counties, housing = 100% → Teachers earning "minimum wage"
3. **V3:** Large counties, housing = 33% → Realistic results ✓

Expect to iterate, but validate early to catch issues sooner.

---

## 🔗 Additional Resources

### Census Bureau
- **ACS API Documentation:** https://www.census.gov/data/developers/data-sets/acs-5year.html
- **ACS Subject Tables:** https://www.census.gov/acs/www/data/data-tables-and-tools/subject-tables/
- **PUMS Data:** https://www.census.gov/programs-surveys/acs/microdata.html

### Cost of Living Data
- **BEA Regional Price Parities:** https://www.bea.gov/data/prices-inflation/regional-price-parities-state-and-metro-area
- **BLS Consumer Expenditure Survey:** https://www.bls.gov/cex/
- **MIT Living Wage Calculator:** https://livingwage.mit.edu/

### Occupation Codes
- **SOC Codes:** https://www.bls.gov/soc/
  - 25-2021: Elementary school teachers
  - 25-2031: Secondary school teachers
  - 25-2051: Special education teachers

### Machine Learning Best Practices
- **Scikit-learn Random Forest:** https://scikit-learn.org/stable/modules/ensemble.html#forest
- **Feature Engineering:** https://www.featuretools.com/
- **Model Validation:** Cross-validation, train-test splits, residual analysis

---

## 📝 Final Thoughts

This analysis demonstrates that **complex data science projects require:**

1. **Clear methodological specifications** in the prompt
2. **Continuous validation** of results against intuition
3. **Documentation** of assumptions and trade-offs
4. **Iteration** with learning from mistakes
5. **Domain knowledge** to avoid reinventing wheels

The optimal prompt combines specificity, validation requirements, and flexibility for iteration. Use this guide as a template for future complex analyses!

---

**Created:** February 2026
**Data Source:** US Census Bureau ACS 2021 5-Year Survey
**Analysis Date:** Based on session conducted February 10, 2026
**Version:** 3.0 (Properly adjusted COL methodology)

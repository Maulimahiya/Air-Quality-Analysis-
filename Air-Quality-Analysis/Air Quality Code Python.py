import pandas as pd

# Option 1: Agar file same folder mein hai jahan Python script hai
df = pd.read_csv(r'C:\Users\mauli\Downloads\air_quality_dataset_12000_rows (1).csv')

print(df.head())
print(f"\nTotal rows: {len(df)}")


# AIR QUALITY PROJECT 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

# Custom colors
PRIMARY_COLOR = '#FF6B6B'
SECONDARY_COLOR = '#4ECDC4'
ACCENT_COLOR = '#45B7D1'

plt.rcParams['figure.figsize'] = (14, 7)
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#F8F9FA'
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11

print("="*70)
print("🌍 AIR QUALITY ANALYSIS PROJECT".center(70))
print("="*70)

# Load data
df = pd.read_csv(r'C:\Users\mauli\Downloads\air_quality_dataset_12000_rows (1).csv')

# Convert Date to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Add useful columns
df['Month'] = df['Date'].dt.month
df['Hour'] = df['Date'].dt.hour
df['Day'] = df['Date'].dt.day

print("\n✅ Data loaded successfully!")
print(f"   📊 Total rows: {df.shape[0]:,}")
print(f"   📋 Columns: {list(df.columns)}")
print(f"   🏙️  Cities: {', '.join(list(df['City'].unique()))}")

print("\n" + "="*70)
print("🏆 TOP 10 MOST POLLUTED CITIES (by PM2.5)".center(70))
print("="*70)

# Calculate average PM2.5 by city
city_pm25 = df.groupby('City')['PM2.5'].mean().sort_values(ascending=False)

# Create a beautiful dataframe display
print("\n📊 City-wise PM2.5 Rankings:")
print("-"*50)
for i, (city, value) in enumerate(city_pm25.items(), 1):
    # Create a visual bar using blocks
    bar_length = int(value / 10)
    bar = "█" * bar_length
    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
    print(f"   {medal} {i}. {city:<12} ▏ {value:>6.2f} µg/m³  {bar}")

print("-"*50)


#BAR CHART
# Create gradient colors (darker to lighter)
colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(city_pm25)))

fig, ax = plt.subplots(figsize=(12, 6))

# Create bars with gradient colors
bars = ax.bar(city_pm25.index, city_pm25.values, color=colors, edgecolor='#2C3E50', linewidth=1.5, alpha=0.9)

# Add value labels on top of bars
for bar, value in zip(bars, city_pm25.values):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1.5,
            f'{value:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#2C3E50')

# Customize chart
ax.set_title('🏆 Most Polluted Cities in India\n(Average PM2.5 Levels)', fontsize=16, fontweight='bold', pad=20, color='#2C3E50')
ax.set_xlabel('City', fontsize=13, fontweight='bold', color='#34495E')
ax.set_ylabel('Average PM2.5 Level (µg/m³)', fontsize=13, fontweight='bold', color='#34495E')
ax.set_xticks(range(len(city_pm25.index)))
ax.set_xticklabels(city_pm25.index, rotation=45, ha='right', fontsize=11)

# Add WHO safe limit line
who_limit = 60
ax.axhline(y=who_limit, color='red', linestyle='--', linewidth=2, alpha=0.7, label=f'WHO Safe Limit: {who_limit} µg/m³')

# Add background grid
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Add legend
ax.legend(loc='upper right', fontsize=10, frameon=True, fancybox=True, shadow=True)

# Add subtle background color
ax.set_facecolor('#FAFAFA')
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.show()

print("\n" + "="*70)
print("✅ ANALYSIS COMPLETED SUCCESSFULLY!".center(70))
print("="*70)

# PART 4: PIE CHART - CITY WISE POLLUTION SHARE
print("\n" + "="*60)
print("CITY WISE PM2.5 POLLUTION SHARE")
print("="*60)

# Calculate total PM2.5 contribution by each city
city_total_pm25 = df.groupby('City')['PM2.5'].sum().sort_values(ascending=False)

# Calculate percentage
city_percentage = (city_total_pm25 / city_total_pm25.sum()) * 100

print("\n📊 City-wise PM2.5 Share:")
for city, pct in city_percentage.items():
    print(f"{city}: {pct:.1f}%")

# SIMPLE PIE CHART
plt.figure(figsize=(10, 8))
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']
explode = (0.05, 0, 0, 0, 0, 0)

plt.pie(city_percentage.values, 
        labels=city_percentage.index, 
        autopct='%1.1f%%',
        colors=colors,
        explode=explode,
        shadow=True,
        startangle=90,
        textprops={'fontsize': 12, 'fontweight': 'bold'})

plt.title('Share of PM2.5 Pollution by City', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()


# PART 5: HYPOTHESIS TESTING (t-test)
# Comparing PM2.5 Levels: Weekday vs Weekend
print("\n" + "="*60)
print("HYPOTHESIS TESTING: Weekday vs Weekend PM2.5 Levels")
print("="*60)

# Add Day of Week column
df['DayOfWeek'] = df['Date'].dt.dayofweek  
# Weekend = Saturday(5) and Sunday(6)
df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')

# Separate data
weekday_pm25 = df[df['IsWeekend'] == 'Weekday']['PM2.5']
weekend_pm25 = df[df['IsWeekend'] == 'Weekend']['PM2.5']

print(f"\n📊 Weekday PM2.5 - Mean: {weekday_pm25.mean():.2f}, Count: {len(weekday_pm25)}")
print(f"📊 Weekend PM2.5 - Mean: {weekend_pm25.mean():.2f}, Count: {len(weekend_pm25)}")

# Perform Independent t-test
t_stat, p_value = stats.ttest_ind(weekday_pm25, weekend_pm25)

print(f"\n📈 T-TEST RESULTS:")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4e}")

print(f"\n📋 CONCLUSION:")
if p_value < 0.05:
    print("✅ Reject Null Hypothesis: Significant difference between Weekday and Weekend PM2.5 levels.")
    if weekday_pm25.mean() > weekend_pm25.mean():
        print("   → Weekdays have HIGHER pollution than Weekends.")
    else:
        print("   → Weekends have HIGHER pollution than Weekdays.")
else:
    print("❌ Fail to Reject Null Hypothesis: No significant difference between Weekday and Weekend PM2.5 levels.")

# Box plot visualization
plt.figure(figsize=(10, 6))
box_data = [weekday_pm25, weekend_pm25]
plt.boxplot(box_data, labels=['Weekday', 'Weekend'], patch_artist=True, 
            boxprops=dict(facecolor='lightblue'), medianprops=dict(color='red', linewidth=2))
plt.title('PM2.5 Levels: Weekday vs Weekend', fontsize=16, fontweight='bold')
plt.ylabel('PM2.5 Level (µg/m³)', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()



# PART 6: CITY-WISE POLLUTANT DISTRIBUTION

print("\n" + "="*60)
print("CITY-WISE POLLUTANT DISTRIBUTION")
print("="*60)

# Calculate average of each pollutant by city
pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
city_pollutants = df.groupby('City')[pollutants].mean()

print("\n📊 Average Pollutant Levels by City:")
print(city_pollutants.round(2))

# GROUPED BAR CHART - Multiple pollutants comparison
fig, ax = plt.subplots(figsize=(14, 7))

x = np.arange(len(city_pollutants.index))
width = 0.13 

# Colors for different pollutants
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# Plot each pollutant
for i, pollutant in enumerate(pollutants):
    ax.bar(x + i*width, city_pollutants[pollutant], width, label=pollutant, color=colors[i])

ax.set_xlabel('City', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Level (µg/m³ for PM/NO2/SO2/O3, mg/m³ for CO)', fontsize=12)
ax.set_title('City-wise Comparison of Different Pollutants', fontsize=16, fontweight='bold')
ax.set_xticks(x + width * 2.5)
ax.set_xticklabels(city_pollutants.index, rotation=45, ha='right')
ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()


# PART 7: MOST CRITICAL POLLUTANTS 
print("\n" + "="*60)
print("MOST CRITICAL POLLUTANTS (Average Across All Cities)")
print("="*60)

# Calculate overall average of each pollutant
pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
overall_avg = df[pollutants].mean().sort_values(ascending=False)

print("\n📊 Most Critical Pollutants (Highest to Lowest Average):")
for pollutant, value in overall_avg.items():
    print(f"{pollutant}: {value:.2f}")

# BAR CHART 
plt.figure(figsize=(12, 7))
bars = plt.bar(overall_avg.index, overall_avg.values, color='teal', edgecolor='black')
plt.title('Most Critical Pollutants (Average Levels Across All Cities)', fontsize=16, fontweight='bold')
plt.xlabel('Pollutant', fontsize=12, fontweight='bold')
plt.ylabel('Average Level', fontsize=12, fontweight='bold')
plt.xticks(rotation=0, fontsize=11)

# Add values on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 1, f'{height:.1f}', 
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()



# PART 8: PM2.5 vs PM10 COMPARISON BY CIT

print("\n" + "="*60)
print("PM2.5 vs PM10 COMPARISON BY CITY")
print("="*60)

# Calculate average PM2.5 and PM10 by city
city_pm25 = df.groupby('City')['PM2.5'].mean()
city_pm10 = df.groupby('City')['PM10'].mean()

# Create a comparison dataframe
comparison_df = pd.DataFrame({
    'PM2.5': city_pm25,
    'PM10': city_pm10
})

print("\n📊 PM2.5 vs PM10 by City:")
print(comparison_df.round(2))

# GROUPED BAR CHART 
fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(comparison_df.index))
width = 0.35

bars1 = ax.bar(x - width/2, comparison_df['PM2.5'], width, label='PM2.5', color='coral', edgecolor='black')
bars2 = ax.bar(x + width/2, comparison_df['PM10'], width, label='PM10', color='skyblue', edgecolor='black')

ax.set_xlabel('City', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Level (µg/m³)', fontsize=12, fontweight='bold')
ax.set_title('PM2.5 vs PM10: Comparison Across Cities', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(comparison_df.index, rotation=45, ha='right')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

# Add values on bars
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2, f'{height:.0f}', ha='center', va='bottom', fontsize=9)

for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2, f'{height:.0f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# SCATTER PLOT: Correlation between PM2.5 and PM10
print("\n" + "="*60)
print("CORRELATION: Are PM2.5 and PM10 Related?")
print("="*60)

plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['PM10'], df['PM2.5'], alpha=0.3, c='purple', edgecolors='black', linewidth=0.5)
plt.xlabel('PM10 Level (µg/m³)', fontsize=12, fontweight='bold')
plt.ylabel('PM2.5 Level (µg/m³)', fontsize=12, fontweight='bold')
plt.title('PM2.5 vs PM10: Correlation Analysis', fontsize=16, fontweight='bold')

# Add trend line
z = np.polyfit(df['PM10'], df['PM2.5'], 1)
p = np.poly1d(z)
plt.plot(df['PM10'].sort_values(), p(df['PM10'].sort_values()), "r--", linewidth=2, label='Trend Line')

# Calculate correlation
correlation = df['PM2.5'].corr(df['PM10'])
plt.text(0.05, 0.95, f'Correlation: {correlation:.3f}', transform=plt.gca().transAxes, 
         fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

print(f"\n📈 Correlation between PM2.5 and PM10: {correlation:.4f}")
if correlation > 0.7:
    print("✅ Strong positive correlation: Cities with high PM10 also have high PM2.5")
elif correlation > 0.4:
    print("📊 Moderate positive correlation")
else:
    print("❌ Weak correlation")



# PART 9: DAY vs NIGHT POLLUTION COMPARISON
print("\n" + "="*60)
print("DAY vs NIGHT POLLUTION COMPARISON")
print("="*60)

# Define Day (6 AM to 6 PM) and Night (6 PM to 6 AM)
df['TimeOfDay'] = df['Hour'].apply(lambda x: 'Day (6AM-6PM)' if 6 <= x < 18 else 'Night (6PM-6AM)')

# Calculate average pollutants by time of day
pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
day_avg = df[df['TimeOfDay'] == 'Day (6AM-6PM)'][pollutants].mean()
night_avg = df[df['TimeOfDay'] == 'Night (6PM-6AM)'][pollutants].mean()

print("\n📊 Day vs Night Pollutant Averages:")
print("\n🌞 DAY TIME (6AM-6PM):")
for p in pollutants:
    print(f"   {p}: {day_avg[p]:.2f}")

print("\n🌙 NIGHT TIME (6PM-6AM):")
for p in pollutants:
    print(f"   {p}: {night_avg[p]:.2f}")

# GROUPED BAR CHART - Day vs Night
fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(pollutants))
width = 0.35

bars1 = ax.bar(x - width/2, day_avg.values, width, label='Day (6AM-6PM)', color='gold', edgecolor='black')
bars2 = ax.bar(x + width/2, night_avg.values, width, label='Night (6PM-6AM)', color='navy', edgecolor='black', alpha=0.7)

ax.set_xlabel('Pollutant', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Level', fontsize=12, fontweight='bold')
ax.set_title('Day vs Night Pollution Comparison', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(pollutants)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

# Add values on bars
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5, f'{height:.1f}', ha='center', va='bottom', fontsize=8)

for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5, f'{height:.1f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# PIE CHART - Overall Share (Day vs Night) 
print("\n" + "="*60)
print("OVERALL POLLUTION SHARE: Day vs Night")
print("="*60)

day_total = df[df['TimeOfDay'] == 'Day (6AM-6PM)']['PM2.5'].sum()
night_total = df[df['TimeOfDay'] == 'Night (6PM-6AM)']['PM2.5'].sum()

day_pct = (day_total / (day_total + night_total)) * 100
night_pct = (night_total / (day_total + night_total)) * 100

print(f"\n🌞 Day Pollution Share: {day_pct:.1f}%")
print(f"🌙 Night Pollution Share: {night_pct:.1f}%")

# Pie Chart
plt.figure(figsize=(8, 8))
labels = ['Day (6AM-6PM)', 'Night (6PM-6AM)']
sizes = [day_pct, night_pct]
colors = ['gold', 'navy']
explode = (0.05, 0)

plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, explode=explode,
        shadow=True, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
plt.title('Overall Pollution Share: Day vs Night', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()



# PART 10: CORRELATION HEATMAP
# (Relationship between different pollutants)
print("\n" + "="*60)
print("CORRELATION HEATMAP - Pollutant Relationships")
print("="*60)

# Select only pollutant columns for correlation
pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
correlation_matrix = df[pollutants].corr()

print("\n📊 Correlation Matrix:")
print(correlation_matrix.round(3))

# Create heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, 
            annot=True,           
            cmap='coolwarm',      
            center=0,
            fmt='.3f',
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            annot_kws={'size': 11, 'fontweight': 'bold'})

plt.title('Pollutant Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right', fontsize=11)
plt.yticks(rotation=0, fontsize=11)
plt.tight_layout()
plt.show()

# Interpretation
print("\n📋 KEY OBSERVATIONS:")
print("-"*40)

# Find highest positive correlation
max_corr = 0
max_pair = ""
for i in range(len(pollutants)):
    for j in range(i+1, len(pollutants)):
        corr = correlation_matrix.iloc[i, j]
        if abs(corr) > max_corr:
            max_corr = abs(corr)
            max_pair = f"{pollutants[i]} & {pollutants[j]}"
print(f"✅ Strongest correlation: {max_pair} ({correlation_matrix.iloc[i, j]:.3f})")

# Check PM2.5 correlations
print(f"\n📌 PM2.5 is most correlated with:")
pm25_corr = correlation_matrix['PM2.5'].sort_values(ascending=False)
for pollutant, corr in pm25_corr.items():
    if pollutant != 'PM2.5':
        print(f"   → {pollutant}: {corr:.3f}")




# PART 19: LINEAR REGRESSION
# Predict PM2.5 using PM10 

print("\n" + "="*70)
print("📈 LINEAR REGRESSION: PM10 → PM2.5 PREDICTION".center(70))
print("="*70)

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


# PREPARE DATA
# Remove missing values
reg_df = df[['PM10', 'PM2.5']].dropna()

# Features (X) and Target (y)
X = reg_df[['PM10']]  # Independent variable
y = reg_df['PM2.5']   # Dependent variable

# Split data into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\n📊 Data Split:")
print(f"   Training data: {len(X_train)} samples")
print(f"   Testing data: {len(X_test)} samples")


# TRAIN THE MODEL

model = LinearRegression()
model.fit(X_train, y_train)

# Get model coefficients
slope = model.coef_[0]
intercept = model.intercept_

print(f"\n📐 Regression Equation:")
print(f"   PM2.5 = {slope:.4f} × PM10 + {intercept:.2f}")


# MAKE PREDICTIONS

y_pred = model.predict(X_test)


# EVALUATE THE MODEL


r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

print(f"\n📊 Model Performance:")
print(f"   R² Score (Accuracy): {r2:.4f}")
print(f"   RMSE: {rmse:.2f}")
print(f"   MAE: {mae:.2f}")

if r2 > 0.7:
    print("   ✅ Strong model - PM10 is a good predictor of PM2.5")
elif r2 > 0.4:
    print("   📊 Moderate model - PM10 somewhat predicts PM2.5")
else:
    print("   ⚠️ Weak model - Other factors also affect PM2.5")


# VISUALIZATION 1: Regression Line

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Scatter plot with regression line
axes[0].scatter(X_test, y_test, alpha=0.4, color='#4ECDC4', label='Actual Data')
axes[0].plot(X_test, y_pred, color='red', linewidth=2, label='Regression Line')
axes[0].set_xlabel('PM10 Level (µg/m³)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('PM2.5 Level (µg/m³)', fontsize=12, fontweight='bold')
axes[0].set_title('Linear Regression: PM10 → PM2.5', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(alpha=0.3, linestyle='--')

# Add equation text
axes[0].text(0.05, 0.95, f'PM2.5 = {slope:.4f} × PM10 + {intercept:.2f}\nR² = {r2:.4f}', 
             transform=axes[0].transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))


# VISUALIZATION 2: Actual vs Predicted

axes[1].scatter(y_test, y_pred, alpha=0.5, color='#45B7D1', edgecolor='black')
axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2, label='Perfect Prediction')
axes[1].set_xlabel('Actual PM2.5 (µg/m³)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Predicted PM2.5 (µg/m³)', fontsize=12, fontweight='bold')
axes[1].set_title('Actual vs Predicted PM2.5', fontsize=14, fontweight='bold')
axes[1].legend()
axes[1].grid(alpha=0.3, linestyle='--')

plt.tight_layout()
plt.show()


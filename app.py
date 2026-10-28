from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="APL Logistics Analytics", page_icon="📦", layout="wide")

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "APL_Logistics.csv"

st.title("📦 APL Logistics Analytics")
st.subheader("Customer, Product, and Profitability Performance Analysis")
st.caption("Unified Mentor | Supply Chain Commercial Intelligence")


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """Load the supplied CSV and normalize column names."""
    try:
        data = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        data = pd.read_csv(path, encoding="latin1")
    data.columns = data.columns.str.strip()
    return data


if not DATA_PATH.exists():
    st.error("Dataset not found. Place APL_Logistics.csv inside the data folder.")
    st.stop()

raw = load_data(str(DATA_PATH))
required = [
    "Sales", "Order Profit Per Order", "Order Item Discount Rate",
    "Order Item Profit Ratio", "Order Customer Id", "Customer Segment",
    "Category Name", "Product Name", "Market", "Order Region",
]
missing_columns = [column for column in required if column not in raw.columns]
if missing_columns:
    st.error("The dataset is missing required columns: " + ", ".join(missing_columns))
    st.stop()

# Convert relevant fields to numeric values where possible.
df = raw.copy()
numeric_cols = [
    "Sales", "Order Profit Per Order", "Order Item Discount",
    "Order Item Discount Rate", "Order Item Profit Ratio", "Order Item Quantity",
    "Order Item Total", "Order Item Product Price", "Product Price",
    "Days for shipping (real)", "Days for shipment (scheduled)",
    "Late_delivery_risk", "Order Customer Id", "Customer Id",
]
for column in numeric_cols:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

# Keep negative-profit rows because they may be genuine loss signals.
# Rows without usable sales/profit values or with non-positive sales are excluded from KPIs.
core_valid = (
    df["Sales"].notna()
    & df["Order Profit Per Order"].notna()
    & (df["Sales"] > 0)
)
analysis = df.loc[core_valid].copy()
analysis["Profit Margin (%)"] = (
    analysis["Order Profit Per Order"] / analysis["Sales"] * 100
)
analysis["Discount Rate (%)"] = analysis["Order Item Discount Rate"] * 100

# Use customer ID as the aggregation key; do not expose names in charts.
if "Order Customer Id" in analysis.columns:
    analysis["Customer Key"] = analysis["Order Customer Id"]
else:
    analysis["Customer Key"] = pd.NA
if "Customer Id" in analysis.columns:
    analysis["Customer Key"] = analysis["Customer Key"].fillna(analysis["Customer Id"])
analysis["Customer Key"] = analysis["Customer Key"].astype("Int64").astype(str)
analysis.loc[analysis["Customer Key"].isin(["<NA>", "nan", "None"]), "Customer Key"] = "Unknown"

st.sidebar.header("Dashboard Filters")
segments = sorted(analysis["Customer Segment"].dropna().astype(str).unique())
selected_segments = st.sidebar.multiselect("Customer segment", segments, default=segments)
categories = sorted(analysis["Category Name"].dropna().astype(str).unique())
selected_categories = st.sidebar.multiselect("Product category", categories, default=categories)
products = sorted(analysis["Product Name"].dropna().astype(str).unique())
selected_products = st.sidebar.multiselect("Product", products, default=products)
markets = sorted(analysis["Market"].dropna().astype(str).unique())
selected_markets = st.sidebar.multiselect("Market", markets, default=markets)
regions = sorted(analysis["Order Region"].dropna().astype(str).unique())
selected_regions = st.sidebar.multiselect("Order region", regions, default=regions)
max_discount = float(analysis["Discount Rate (%)"].dropna().max()) if analysis["Discount Rate (%)"].notna().any() else 0.0
discount_limit = st.sidebar.slider(
    "Maximum discount rate (%)", 0.0, max(100.0, max_discount),
    min(100.0, max_discount), 1.0,
)

filtered = analysis.copy()
filtered = filtered[filtered["Customer Segment"].astype(str).isin(selected_segments)]
filtered = filtered[filtered["Category Name"].astype(str).isin(selected_categories)]
filtered = filtered[filtered["Product Name"].astype(str).isin(selected_products)]
filtered = filtered[filtered["Market"].astype(str).isin(selected_markets)]
filtered = filtered[filtered["Order Region"].astype(str).isin(selected_regions)]
filtered = filtered[filtered["Discount Rate (%)"].fillna(0) <= discount_limit]

if filtered.empty:
    st.warning("No data matches your selected filters. Select more values in the sidebar.")
    st.stop()


def money(value: float) -> str:
    """Format a numeric value for display; source currency is unspecified."""
    return f"${value:,.2f}"


def margin_percent(profit: float, revenue: float) -> float:
    return (profit / revenue * 100) if revenue else 0.0


total_revenue = float(filtered["Sales"].sum())
total_profit = float(filtered["Order Profit Per Order"].sum())
overall_margin = margin_percent(total_profit, total_revenue)
customer_count = int(filtered["Customer Key"].nunique())
item_count = len(filtered)
customer_value_index = total_profit / customer_count if customer_count else 0.0

# Assignment defines Category Margin as the average margin by product category.
# Calculate each selected category's margin, then average those category margins.
category_kpi = filtered.groupby("Category Name", dropna=False).agg(
    Category_Revenue=("Sales", "sum"),
    Category_Profit=("Order Profit Per Order", "sum"),
)
category_kpi["Category_Margin (%)"] = (
    category_kpi["Category_Profit"]
    / category_kpi["Category_Revenue"].replace(0, pd.NA)
    * 100
)
category_margin = (
    float(category_kpi["Category_Margin (%)"].dropna().mean())
    if category_kpi["Category_Margin (%)"].notna().any()
    else 0.0
)

# Discount Impact Ratio is defined here as discount amount divided by revenue.
# It describes the recorded discount burden, not a causal effect on profit.
if "Order Item Discount" in filtered.columns:
    total_discount = float(pd.to_numeric(filtered["Order Item Discount"], errors="coerce").fillna(0).sum())
else:
    total_discount = 0.0
discount_impact_ratio = (total_discount / total_revenue * 100) if total_revenue else 0.0

k1, k2, k3 = st.columns(3)
k1.metric("Total Revenue", money(total_revenue))
k2.metric("Total Profit", money(total_profit))
k3.metric("Profit Margin %", f"{overall_margin:.2f}%")
k4, k5, k6 = st.columns(3)
k4.metric("Customer Value Index", money(customer_value_index))
k5.metric("Category Margin", f"{category_margin:.2f}%")
k6.metric("Discount Burden Ratio", f"{discount_impact_ratio:.2f}%")
st.caption(
    f"Showing {item_count:,} rows after filters and {customer_count:,} unique customers. "
    "Currency is displayed as $ for presentation; the source file does not specify a currency. "
    "CVI is defined as total recorded profit divided by unique customers. Category Margin is the "
    "unweighted average of the selected categories' individual margins. Discount Burden Ratio is "
    "total recorded discount divided by revenue; it is a proxy, not a causal estimate of margin loss."
)

# The source file has no order-date column, so do not fabricate a time trend.
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Revenue & Profit", "Customer Value", "Product & Category",
    "Discount Impact", "Market & Data Quality",
])

with tab1:
    st.header("Revenue & Profit Overview")
    left, right = st.columns(2)
    with left:
        rev_profit = pd.DataFrame({
            "Metric": ["Revenue", "Profit"],
            "Amount": [total_revenue, total_profit],
        })
        fig = px.bar(
            rev_profit, x="Metric", y="Amount", color="Metric",
            title="Total Revenue vs Total Profit", text_auto=True,
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        if "Order Status" in filtered.columns:
            status = filtered.groupby("Order Status", dropna=False)["Sales"].sum().reset_index()
            fig = px.bar(
                status, x="Order Status", y="Sales",
                title="Revenue by Order Status", text_auto=True,
            )
            fig.update_layout(xaxis_title="Order status", yaxis_title="Revenue")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Order status is not available in this dataset.")

    st.subheader("Financial summary")
    summary = pd.DataFrame({
        "Metric": ["Rows included", "Revenue", "Profit", "Profit margin", "Negative-profit rows"],
        "Value": [
            f"{len(filtered):,}", money(total_revenue), money(total_profit),
            f"{overall_margin:.2f}%",
            f"{(filtered['Order Profit Per Order'] < 0).sum():,}",
        ],
    })
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.info(
        "The source dataset has no order-date field, so a true daily/monthly margin trend "
        "cannot be calculated. Available non-date dimensions are shown instead."
    )

with tab2:
    st.header("Customer Value Dashboard")
    cust = filtered.groupby("Customer Key", dropna=False).agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Rows=("Sales", "size"),
    ).reset_index()
    cust["Margin (%)"] = (cust["Profit"] / cust["Revenue"].replace(0, pd.NA) * 100).fillna(0)
    cust["Customer Label"] = "Customer " + cust["Customer Key"].astype(str)
    if len(cust) >= 3:
        cust["Value Tier"] = pd.qcut(
            cust["Profit"].rank(method="first"), q=3,
            labels=["Low", "Medium", "High"],
        )
    else:
        cust["Value Tier"] = "Not enough customers to tier"

    left, right = st.columns(2)
    with left:
        st.subheader("Top 10 customers by profit")
        top = cust.nlargest(10, "Profit").sort_values("Profit")
        fig = px.bar(
            top, x="Profit", y="Customer Label", orientation="h",
            hover_data=["Customer Key", "Revenue", "Margin (%)"],
            title="Highest-profit customers",
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Bottom 10 customers by profit")
        bottom = cust.nsmallest(10, "Profit").sort_values("Profit", ascending=False)
        fig = px.bar(
            bottom, x="Profit", y="Customer Label", orientation="h",
            color="Profit", color_continuous_scale="RdYlGn",
            hover_data=["Customer Key", "Revenue", "Margin (%)"],
            title="Lowest-profit customers",
        )
        st.plotly_chart(fig, use_container_width=True)

    seg = filtered.groupby("Customer Segment", dropna=False).agg(
        Revenue=("Sales", "sum"), Profit=("Order Profit Per Order", "sum")
    ).reset_index()
    seg["Margin (%)"] = seg["Profit"] / seg["Revenue"].replace(0, pd.NA) * 100
    st.subheader("Customer segment contribution")
    st.plotly_chart(
        px.bar(seg, x="Customer Segment", y=["Revenue", "Profit"], barmode="group",
               title="Revenue and profit by customer segment"),
        use_container_width=True,
    )
    st.caption(
        "Customer Value Index is total recorded profit divided by unique customers. "
        "Customer ranking uses aggregated profit by customer ID."
    )

with tab3:
    st.header("Product & Category Performance")
    category = filtered.groupby("Category Name", dropna=False).agg(
        Revenue=("Sales", "sum"), Profit=("Order Profit Per Order", "sum"),
        Items=("Sales", "size"),
    ).reset_index()
    category["Margin (%)"] = category["Profit"] / category["Revenue"].replace(0, pd.NA) * 100
    left, right = st.columns(2)
    with left:
        st.subheader("Category profitability")
        fig = px.bar(
            category.sort_values("Profit", ascending=False).head(15),
            x="Category Name", y="Profit", color="Margin (%)",
            title="Top 15 categories by total profit", hover_data=["Revenue", "Margin (%)"],
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Category margin comparison")
        heat = category.sort_values("Margin (%)", ascending=True)
        fig = px.bar(
            heat, x="Margin (%)", y="Category Name", orientation="h",
            title="Profit margin by category", hover_data=["Revenue", "Profit"],
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Products: high revenue but low margin")
    product = filtered.groupby("Product Name", dropna=False).agg(
        Revenue=("Sales", "sum"), Profit=("Order Profit Per Order", "sum")
    ).reset_index()
    product["Margin (%)"] = product["Profit"] / product["Revenue"].replace(0, pd.NA) * 100
    if len(product) >= 2:
        low_margin_cutoff = float(product["Margin (%)"].quantile(0.25))
        high_revenue_cutoff = float(product["Revenue"].quantile(0.75))
        risk = product[
            (product["Revenue"] >= high_revenue_cutoff)
            & (product["Margin (%)"] <= low_margin_cutoff)
        ].sort_values("Revenue", ascending=False)
        st.caption(
            "Rule used: revenue at or above the 75th percentile and margin at or below the "
            "25th percentile. This is a relative screening rule, not a universal business threshold."
        )
        if risk.empty:
            st.success("No products meet the current high-revenue / low-margin screening rule.")
        else:
            st.dataframe(risk, use_container_width=True, hide_index=True)
    else:
        st.info("At least two products are needed for the high-revenue / low-margin comparison.")

    loss_categories = category[category["Profit"] < 0].sort_values("Profit")
    st.subheader("Loss-making categories")
    if loss_categories.empty:
        st.success("No categories have negative total profit under the current filters.")
    else:
        st.dataframe(loss_categories, use_container_width=True, hide_index=True)

with tab4:
    st.header("Discount Impact Analyzer")
    st.caption(
        "Discounted and non-discounted records may differ in product mix and other factors. "
        "The comparison shows association, not proof that discounts caused the margin difference."
    )

    # Required diagnostic: compare rows with a recorded discount against rows with no discount.
    discount_compare = filtered.dropna(subset=["Discount Rate (%)"]).copy()
    discount_compare["Discount Status"] = discount_compare["Discount Rate (%)"].gt(0).map(
        {True: "Discounted", False: "No discount"}
    )
    if not discount_compare.empty:
        discount_summary = discount_compare.groupby("Discount Status", dropna=False).agg(
            Rows=("Sales", "size"),
            Revenue=("Sales", "sum"),
            Profit=("Order Profit Per Order", "sum"),
            Average_Discount_Rate=("Discount Rate (%)", "mean"),
        ).reset_index()
        discount_summary["Profit Margin (%)"] = (
            discount_summary["Profit"]
            / discount_summary["Revenue"].replace(0, pd.NA)
            * 100
        )
        discount_summary["Average Discount Rate (%)"] = discount_summary[
            "Average_Discount_Rate"
        ]
        st.subheader("Discounted vs. non-discounted performance")
        st.dataframe(
            discount_summary[
                ["Discount Status", "Rows", "Revenue", "Profit",
                 "Profit Margin (%)", "Average Discount Rate (%)"]
            ].round(2),
            use_container_width=True,
            hide_index=True,
        )
        compare_chart = discount_summary.melt(
            id_vars="Discount Status",
            value_vars=["Profit Margin (%)"],
            var_name="Metric",
            value_name="Percentage",
        )
        fig = px.bar(
            compare_chart,
            x="Discount Status",
            y="Percentage",
            title="Profit margin: discounted vs. non-discounted records",
            text_auto=True,
        )
        fig.update_layout(yaxis_title="Profit margin (%)", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No usable discount-rate values are available for this comparison.")

    left, right = st.columns(2)
    with left:
        st.subheader("Discount rate vs profit ratio")
        scatter = filtered.dropna(subset=["Discount Rate (%)", "Order Item Profit Ratio"])
        if len(scatter) > 6000:
            scatter = scatter.sample(6000, random_state=42)
        if not scatter.empty:
            fig = px.scatter(
                scatter, x="Discount Rate (%)", y="Order Item Profit Ratio",
                color="Order Item Profit Ratio", opacity=0.6,
                title="Discount rate vs order-item profit ratio",
                hover_data=["Category Name", "Product Name", "Sales"],
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No usable discount/profit-ratio values are available under these filters.")

    with right:
        st.subheader("Average margin by discount band")
        bands = filtered.dropna(subset=["Discount Rate (%)"]).copy()
        if not bands.empty:
            bands["Discount Band"] = pd.cut(
                bands["Discount Rate (%)"],
                bins=[-0.001, 5, 10, 15, 20, 30, 50, 100.001],
                labels=["0–5%", "5–10%", "10–15%", "15–20%", "20–30%", "30–50%", "50%+"],
                include_lowest=True,
            )
            band_summary = bands.groupby("Discount Band", observed=False).agg(
                Rows=("Sales", "size"), Revenue=("Sales", "sum"),
                Profit=("Order Profit Per Order", "sum"),
            ).reset_index()
            band_summary["Margin (%)"] = (
                band_summary["Profit"] / band_summary["Revenue"].replace(0, pd.NA) * 100
            )
            fig = px.bar(
                band_summary, x="Discount Band", y="Margin (%)",
                hover_data=["Rows", "Revenue", "Profit"],
                title="Profit margin by discount band",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No discount-rate values are available under the current filters.")

    st.subheader("What-if discount scenario")
    st.write(
        "This is a simplified scenario calculator. It estimates the effect of an additional "
        "discount on current revenue, assuming units and underlying costs stay constant. "
        "It is not a causal forecast."
    )
    extra_discount = st.slider(
        "Additional discount to test (%)", 0.0, 30.0, 5.0, 0.5, key="what_if_discount"
    )
    reduction = total_revenue * extra_discount / 100
    scenario_revenue = total_revenue - reduction
    scenario_profit = total_profit - reduction
    scenario_margin = margin_percent(scenario_profit, scenario_revenue)
    a, b, c = st.columns(3)
    a.metric("Scenario revenue", money(scenario_revenue), delta=money(-reduction))
    b.metric("Scenario profit", money(scenario_profit), delta=money(-reduction))
    c.metric("Scenario margin", f"{scenario_margin:.2f}%")
    st.caption(
        "Scenario assumption: the extra discount reduces revenue and profit by the same amount. "
        "Use for sensitivity discussion only; a real pricing model needs unit costs and demand assumptions."
    )

with tab5:
    st.header("Market, Regional Profit & Data Quality")
    left, right = st.columns(2)
    with left:
        market = filtered.groupby("Market", dropna=False).agg(
            Revenue=("Sales", "sum"), Profit=("Order Profit Per Order", "sum")
        ).reset_index().sort_values("Profit", ascending=False)
        market["Margin (%)"] = market["Profit"] / market["Revenue"].replace(0, pd.NA) * 100
        st.subheader("Profit by market")
        fig = px.bar(
            market, x="Market", y="Profit", color="Margin (%)",
            title="Market profit and margin", hover_data=["Revenue"],
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        region = filtered.groupby("Order Region", dropna=False).agg(
            Revenue=("Sales", "sum"), Profit=("Order Profit Per Order", "sum")
        ).reset_index().sort_values("Profit", ascending=False)
        region["Margin (%)"] = region["Profit"] / region["Revenue"].replace(0, pd.NA) * 100
        st.subheader("Profit by order region")
        fig = px.bar(
            region, x="Order Region", y="Profit", title="Regional profit",
            hover_data=["Revenue", "Margin (%)"],
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Country profitability")
    if "Order Country" in filtered.columns:
        country = filtered.groupby("Order Country", dropna=False).agg(
            Revenue=("Sales", "sum"), Profit=("Order Profit Per Order", "sum")
        ).reset_index()
        country["Margin (%)"] = country["Profit"] / country["Revenue"].replace(0, pd.NA) * 100
        st.dataframe(
            country.sort_values("Profit", ascending=False).head(20),
            use_container_width=True, hide_index=True,
        )

    st.subheader("Data quality checks")
    dq = pd.DataFrame({
        "Check": [
            "Rows in original dataset", "Rows used in financial analysis",
            "Rows excluded for missing/non-positive sales or missing profit",
            "Duplicate full rows", "Missing Sales", "Missing Order Profit Per Order",
            "Negative-profit rows in analysis",
        ],
        "Result": [
            f"{len(raw):,}", f"{len(analysis):,}", f"{len(raw) - len(analysis):,}",
            f"{raw.duplicated().sum():,}", f"{raw['Sales'].isna().sum():,}",
            f"{raw['Order Profit Per Order'].isna().sum():,}",
            f"{(analysis['Order Profit Per Order'] < 0).sum():,}",
        ],
    })
    st.dataframe(dq, use_container_width=True, hide_index=True)
    st.caption(
        "Negative-profit rows are retained because they may represent genuine loss-making records. "
        "Customer names and street addresses exist in the source dataset; avoid publishing personal "
        "details in public screenshots or reports."
    )

st.divider()
st.caption(
    "Built with Python, Pandas, Plotly and Streamlit. Dashboard figures update with the sidebar filters. "
    "Financial totals are calculated by summing source rows; verify the meaning of 'Order Profit Per Order' "
    "in the dataset documentation before interpreting the totals as distinct-order profit."
)
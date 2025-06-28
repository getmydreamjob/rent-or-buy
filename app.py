import streamlit as st

def calculate_rent_cost(rent, rent_increase, insurance, years):
    total_rent = 0
    current_rent = rent
    for year in range(1, years + 1):
        total_rent += current_rent * 12
        current_rent *= (1 + rent_increase / 100)
    total_insurance = insurance * years
    return total_rent + total_insurance, total_rent, total_insurance

def calculate_buy_cost(price, down_payment, mortgage_rate, loan_term, tax, insurance, maintenance_pct, appreciation, years, sell_cost_pct):
    loan = price - down_payment
    monthly_rate = mortgage_rate / 100 / 12
    n_payments = loan_term * 12
    monthly_payment = loan * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
    
    total_mortgage_paid = monthly_payment * 12 * years
    principal_paid = 0
    balance = loan
    
    for _ in range(years * 12):
        interest = balance * monthly_rate
        principal = monthly_payment - interest
        principal_paid += principal
        balance -= principal

    property_tax = tax * years
    home_insurance = insurance * years
    maintenance = maintenance_pct / 100 * price * years
    
    home_value = price * (1 + appreciation / 100) ** years
    selling_cost = sell_cost_pct / 100 * home_value
    net_proceeds = home_value - balance - selling_cost

    total_out_of_pocket = total_mortgage_paid + property_tax + home_insurance + maintenance + selling_cost - net_proceeds
    return {
        'total_mortgage_paid': total_mortgage_paid,
        'property_tax': property_tax,
        'home_insurance': home_insurance,
        'maintenance': maintenance,
        'selling_cost': selling_cost,
        'net_proceeds': net_proceeds,
        'total_out_of_pocket': total_out_of_pocket,
        'monthly_payment': monthly_payment
    }

st.title("🏠 Rent vs Buy Calculator")

st.markdown("Enter your details below to see which option might be better for you.")

st.header("📌 Rent Info")
rent = st.number_input("Monthly rent ($)", value=2500)
rent_increase = st.number_input("Annual rent increase (%)", value=3.0)
rent_insurance = st.number_input("Renters insurance per year ($)", value=200)

st.header("📌 Buy Info")
price = st.number_input("Home price ($)", value=600000)
down_payment = st.number_input("Down payment ($)", value=120000)
mortgage_rate = st.number_input("Mortgage rate (%)", value=6.5)
loan_term = st.number_input("Loan term (years)", value=30)
property_tax = st.number_input("Property tax per year ($)", value=6000)
home_insurance = st.number_input("Homeowners insurance per year ($)", value=1500)
maintenance_pct = st.number_input("Annual maintenance (% of home value)", value=1.0)
appreciation = st.number_input("Home appreciation (%)", value=3.0)
sell_cost_pct = st.number_input("Selling cost (% of final home price)", value=7.0)

st.header("⏳ Time")
years = st.slider("Years you plan to stay", 1, 30, 7)

if st.button("Check Rent or Buy"):
    rent_cost, rent_only, rent_ins = calculate_rent_cost(rent, rent_increase, rent_insurance, years)
    buy_result = calculate_buy_cost(price, down_payment, mortgage_rate, loan_term, property_tax, home_insurance, maintenance_pct, appreciation, years, sell_cost_pct)
    
    if rent_cost < buy_result['total_out_of_pocket']:
        st.success("✅ Renting is likely cheaper over this period based on your inputs.")
    else:
        st.success("✅ Buying is likely cheaper over this period based on your inputs.")
    
    with st.expander("See detailed calculation"):
        st.markdown("### Rent Summary")
        st.write(f"Total rent paid: ${rent_only:,.0f}")
        st.write(f"Total renters insurance: ${rent_ins:,.0f}")
        st.write(f"**Total cost of renting:** ${rent_cost:,.0f}")

        st.markdown("### Buy Summary")
        st.write(f"Monthly mortgage payment: ${buy_result['monthly_payment']:,.0f}")
        st.write(f"Total mortgage payments: ${buy_result['total_mortgage_paid']:,.0f}")
        st.write(f"Property taxes: ${buy_result['property_tax']:,.0f}")
        st.write(f"Home insurance: ${buy_result['home_insurance']:,.0f}")
        st.write(f"Maintenance cost: ${buy_result['maintenance']:,.0f}")
        st.write(f"Selling cost: ${buy_result['selling_cost']:,.0f}")
        st.write(f"Net proceeds from sale: ${buy_result['net_proceeds']:,.0f}")
        st.write(f"**Total out-of-pocket cost of buying:** ${buy_result['total_out_of_pocket']:,.0f}")

        st.markdown("### Pros of Renting")
        st.write("- Flexibility to move without selling")
        st.write("- No maintenance headaches")
        st.write("- Lower upfront cost")

        st.markdown("### Pros of Buying")
        st.write("- Build equity over time")
        st.write("- Potential property appreciation")
        st.write("- More stable housing costs long-term")

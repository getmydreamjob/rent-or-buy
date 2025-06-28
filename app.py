import streamlit as st

def parse_input(text):
    try:
        return float(text)
    except:
        return 0.0

def calculate_rent_cost(rent, rent_increase, insurance, years):
    total_rent = 0
    current_rent = rent
    for year in range(1, years + 1):
        total_rent += current_rent * 12
        current_rent *= (1 + rent_increase / 100)
    total_insurance = insurance * years
    return total_rent + total_insurance, total_rent, total_insurance

def calculate_buy_cost(price, down_payment_pct, mortgage_rate, loan_term, tax, insurance, maintenance, appreciation, years, sell_cost_pct):
    down_payment = price * (down_payment_pct / 100)
    loan = price - down_payment
    monthly_rate = mortgage_rate / 100 / 12
    n_payments = loan_term * 12
    if monthly_rate > 0:
        monthly_payment = loan * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
    else:
        monthly_payment = loan / n_payments
    
    total_mortgage_paid = monthly_payment * 12 * years
    balance = loan
    
    for _ in range(years * 12):
        interest = balance * monthly_rate
        principal = monthly_payment - interest
        balance -= principal

    property_tax = tax * years
    home_insurance = insurance * years
    maintenance_total = maintenance * years
    
    home_value = price * (1 + appreciation / 100) ** years
    selling_cost = sell_cost_pct / 100 * home_value
    net_proceeds = home_value - balance - selling_cost

    total_out_of_pocket = total_mortgage_paid + property_tax + home_insurance + maintenance_total + selling_cost - net_proceeds
    return {
        'down_payment': down_payment,
        'total_mortgage_paid': total_mortgage_paid,
        'property_tax': property_tax,
        'home_insurance': home_insurance,
        'maintenance_total': maintenance_total,
        'selling_cost': selling_cost,
        'net_proceeds': net_proceeds,
        'total_out_of_pocket': total_out_of_pocket,
        'monthly_payment': monthly_payment
    }

st.title("🏠 Rent vs Buy Calculator")

st.markdown("Enter your details below to see which option might be better for you.")

st.header("📌 Rent Info")
rent = parse_input(st.text_input("Monthly rent ($)", placeholder="e.g. 2500", help="Enter your current monthly rent amount in dollars."))
rent_increase = parse_input(st.text_input("Annual rent increase (%)", placeholder="e.g. 3", help="Expected yearly rent increase as a percentage."))
rent_insurance = parse_input(st.text_input("Renters insurance per year ($)", placeholder="e.g. 200", help="Yearly cost of your renters insurance."))

st.header("📌 Buy Info")
price = parse_input(st.text_input("Home price ($)", placeholder="e.g. 600000", help="Total price of the home you want to buy."))
down_payment_pct = parse_input(
    st.text_input(
        "Down payment (%)", 
        placeholder="e.g. 20", 
        help="Enter the down payment as a percentage of home price."
    )
)
mortgage_rate = parse_input(st.text_input("Mortgage rate (%)", placeholder="e.g. 6.5", help="Your mortgage's annual interest rate percentage."))
loan_term = parse_input(st.text_input("Loan term (years)", placeholder="e.g. 30", help="Number of years for your mortgage loan."))
property_tax = parse_input(st.text_input("Property tax per year ($)", placeholder="e.g. 6000", help="Annual property tax amount."))
home_insurance = parse_input(st.text_input("Homeowners insurance per year ($)", placeholder="e.g. 1500", help="Yearly cost of your homeowners insurance."))
maintenance = parse_input(st.text_input("Annual maintenance ($)", placeholder="e.g. 6000", help="Enter annual maintenance cost in dollars."))
appreciation = parse_input(st.text_input("Home appreciation (%)", placeholder="e.g. 3", help="Expected annual home value growth percentage."))
sell_cost_pct = parse_input(st.text_input("Selling cost (% of final home price)", placeholder="e.g. 7", help="Percentage of home price lost to selling costs when you sell."))

st.header("⏳ Time")
years = st.slider("Years you plan to stay", 1, 30, 7)

if st.button("Check Rent or Buy"):
    rent_cost, rent_only, rent_ins = calculate_rent_cost(rent, rent_increase, rent_insurance, years)
    buy_result = calculate_buy_cost(price, down_payment_pct, mortgage_rate, loan_term, property_tax, home_insurance, maintenance, appreciation, years, sell_cost_pct)
    
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
        st.write(f"Down payment: ${buy_result['down_payment']:,.0f}")
        st.write(f"Monthly mortgage payment: ${buy_result['monthly_payment']:,.0f}")
        st.write(f"Total mortgage payments: ${buy_result['total_mortgage_paid']:,.0f}")
        st.write(f"Property taxes: ${buy_result['property_tax']:,.0f}")
        st.write(f"Home insurance: ${buy_result['home_insurance']:,.0f}")
        st.write(f"Maintenance cost (total): ${buy_result['maintenance_total']:,.0f}")
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

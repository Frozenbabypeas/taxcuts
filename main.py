import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from calc import *

st.set_page_config(page_title = "Stage 3 Tax Simplified", layout = "centered", page_icon=':money_with_wings:')

def main():
    st.title("Rethinking Stage 3 Tax Reform: Assessing the Impact")
    with st.container():
        st.markdown("""
        **Disclaimer:** *This app is for educational purposes only.  The information provided by the app is not intended to be a substitute for professional advice and relied on for your personal tax affairs.  Use the information at your own risk.  For more information on the bill, it can be found [here](  
        https://parlinfo.aph.gov.au/parlInfo/search/display/display.w3p;query=Id%3A%22legislation%2Fems%2Fr7140_ems_f51c76c0-555b-4aff-b345-9c70f361cfc7%22;rec=0).*
        """)
        st.text("")
        st.markdown("""               
        Below is a graph  on government revenue recieved from Individual Taxable income with the forward estimates.  You can find this data [here](https://budget.gov.au/content/bp1/index.htm).
        """)
        st.subheader("Government Revenue received over the last 20 years")
        # Load the CSV file
        file_path = "Government Receipts.csv" 
        gdf = load_data(file_path) 

        x = gdf['Government Revenue']
        y = gdf['Total individuals and other withholding']
        y1 = gdf['Projected']
                    
        # Create a figure and axis object
        fig, ax = plt.subplots()

        # Plot the data
        ax.plot(x, y1, label='Projected Revenue', color = 'red', linestyle = '--')
        ax.plot(x, y, label='Government Revenue')
        

        # Customize the plot
        ax.set_xlabel('Years')
        ax.set_ylabel('Dollars')
        ax.legend()
        ax.set_yticklabels([])
        ax.set_xticklabels([])

        # Annotated notes
        ax.annotate('2008', xy=(2, 125992), xytext=(2, 150000),
                    arrowprops=dict(facecolor='black', shrink=0.1, width = 0.05, headwidth = 3))
        ax.annotate('2012', xy=(7, 160203), xytext=(7, 200000),
            arrowprops=dict(facecolor='black', shrink=0.1, width = 0.05, headwidth = 3))
        ax.annotate('2018', xy=(14, 228445), xytext=(14, 150000),
            arrowprops=dict(facecolor='black', shrink=0.1, width = 0.05, headwidth = 3))
        ax.annotate('We are here', xy=(17, 303200), xytext=(17, 200000),
            arrowprops=dict(facecolor='black', shrink=0.1, width = 0.05, headwidth = 3))

        # Display the plot in Streamlit
        st.pyplot(fig)
        st.markdown("""
        Summary of the last 20 years related to income tax:
                                
        - 2008 - Liberal Government introduces LITO as part of major tax reform changes.
        - 2012 - Labor Government increased the tax free theshold from 6,000 to 18,200.
        - 2018 - Liberal Government introduces Tax Reform in 3 stages.
        
        The large spike after 2018 in revenue occured after major tax reform was first introduced and the stages 1 to 3 were being phased in.  People generally pay into the tax system with a higher rate of compliance when the tax system is simplier.
        
        """)
    
    st.subheader("Are you better or worse off ?")
    # Input fields
    col1, col2 = st.columns(2)
    with col1:
        taxable_income = st.text_input("Taxable Income:")

    with col2:
        user_type = st.radio("Select income type:", ["Resident", "Non Resident","Holiday Maker", ])

    # convert input to numbers
    try:
        taxable_income = float(taxable_income)
    except:
        st.error("Only Numbers")
        return
    
    if st.button('Net effect from the ATO Reaper', key = 'calculations', use_container_width= 500):
        # Calculate tax
        original = int(stage3tax2025(taxable_income))
        proposed = int(proposedtax2025(taxable_income))
        non_resident = int(nrtax2025(taxable_income))
        proposed_non_resident = int(proposed_nrtax2025(taxable_income))
        holidaymaker = int(hmtax2025(taxable_income))
        proposed_holidamaker = int(proposed_hmtax2025(taxable_income))
        lito2025 = int(lito(taxable_income))
        lmito2025= int(litmo(taxable_income))
        medicare = int(medicare2025(taxable_income))
        proposed_medicare = int(proposed_medicare2025(taxable_income))
        difference = (original + medicare) - (proposed + proposed_medicare)
        difference_nr = (non_resident) - (proposed_non_resident)
        difference_hm = holidaymaker - proposed_holidamaker

        with st.container():
            st.subheader("Tax cut differences")
        
        color = 'green' if difference >=0 else 'red'

        if user_type == "Resident":

            with st.container():
                st.markdown("""
                <style>
                    .st-curve {
                        border-radius: 10px;
                        border: 1px solid #8E9DCC;
                        padding: 10px;
                        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.2);
                        font-size: 16px;
                    }
                </style>
                """, unsafe_allow_html = True)
                st.markdown(f"""
                    <div class="st-curve">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div></div>
                            <div></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div>Tax Liability including the Medicare levy (Liberal)</div>
                            <div>${original+medicare:,}</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div>Revised Tax Liability including the proposed changes to the Medicare levy (Labor)</div>
                            <div>${proposed+proposed_medicare:,}</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div style="color: {color}">Difference ({"Better off" if difference >= 0 else "Worse off"})</div>
                            <div style="color : {'green' if  difference >= 0 else 'red'}">${abs(difference):,}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        elif user_type == "Non Resident":
            
            with st.container():
                st.markdown("""
                <style>
                    .st-curve {
                        border-radius: 10px;
                        border: 1px solid #8E9DCC;
                        padding: 10px;
                        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.2);
                        font-size: 16px;
                    }
                </style>
                """, unsafe_allow_html = True)
                st.markdown(f"""
                    <div class="st-curve">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div></div>
                            <div></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div>Tax Liability (Liberal)</div>
                            <div>${non_resident:,}</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div>Revised Tax Liability (Labor)</div>
                            <div>${proposed_non_resident:,}</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div style="color: {color}">Difference ({"Better off" if difference_nr >= 0 else "Worse off"})</div>
                            <div style="color : {'green' if  difference_nr >= 0 else 'red'}">${abs(difference_nr):,}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        else:
            
            with st.container():
                st.markdown("""
                <style>
                    .st-curve {
                        border-radius: 10px;
                        border: 1px solid #8E9DCC;
                        padding: 10px;
                        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.2);
                        font-size: 16px;
                    }
                </style>
                """, unsafe_allow_html = True)
                st.markdown(f"""
                    <div class="st-curve">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div></div>
                            <div></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div>Tax Liability (Liberal)</div>
                            <div>${holidaymaker:,}</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div>Revised Tax Liability (Labor)</div>
                            <div>${proposed_holidamaker:,}</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div style="color: {color}">Difference ({"Better off" if difference_hm >= 0 else "Worse off"})</div>
                            <div style="color : {'green' if  difference_hm >= 0 else 'red'}">${abs(difference_hm):,}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.text("")
        st.subheader("Pain overview:")           
        st.text("")                 
        taxable_income_range, prior_liability, tax_liability, proposed_tax_liability = tax_chart()
                
        data = {'Taxable Income': taxable_income_range,
                'Current Tax Rates (2024)': prior_liability,
                'Stage 3 Tax Cuts (Liberal)': tax_liability,
                'Proposed Stage 3 Tax Cuts (Labor)': proposed_tax_liability
                }
            
        df = pd.DataFrame(data)
        st.dataframe(df, width = 800)
        st.text("")
        st.subheader("Pain Train:")           
        st.text("")
        fig, ax = plt.subplots()
        # st.line_chart(df.set_index('Taxable Income'), x='Taxablele Income')
        ax.plot(df['Taxable Income'], df['Current Tax Rates (2024)'], label='Current Tax Rates (2024)')
        ax.plot(df['Taxable Income'], df['Stage 3 Tax Cuts (Liberal)'], label='Stage 3 Tax Cuts (Liberal)')
        ax.plot(df['Taxable Income'], df['Proposed Stage 3 Tax Cuts (Labor)'], label='Proposed Stage 3 Tax Cuts (Labor)')

        # Customize the plot
        ax.set_xlabel('Taxable Income')
        ax.set_ylabel('Tax Liability')
        ax.set_title('Tax Liability Comparison')
        ax.legend()

        # Display the plot using st.pyplot
        st.pyplot(fig)
        # st.text("")
        # st.markdown("""
        # **Revised calculation** - Changes in Lmito and Lito to provide the same results:
        # """)

        # target_litmo = 1000
        # result_taxable_income = goal_seek(target_litmo)

        # st.text(f"The taxable income for a LITMO of {target_litmo} is approximately: {result_taxable_income}")

        # st.text("")
        # st.subheader("Lets add in the affect of Lito and Lmito")
        # st.text("")
        # st.markdown(f"""
        #     <div class="st-curve">
        #         <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
        #             <div></div>
        #             <div></div>
        #         </div>
        #         <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
        #             <div>(Proposed) New tax Liability</div>
        #             <div>${original+medicare-lito2025-lmito2025:,}</div>
        #         </div>
        #     </div>
        #     """, unsafe_allow_html=True)

        st.text("")
        with st.container():
            st.subheader("This proposal in a nutshell:") 
            st.markdown("""                               
            The [Personal Income Tax Plan](https://archive.budget.gov.au/2018-19/factsheets/lower-simpler-fairer-taxes.pdf), established in 2018, was designed for the following reason:
                
            >The Government is building a personal tax system that encourages aspirational Australians to get ahead while being fiscally responsible. The first step will provide tax relief to low and middle income earners, the second step will help tackle bracket creep and the third step will simplify and flatten the system. Together our reforms to company taxes, tax integrity and personal income taxes will build a simpler tax system, reward hardworking Australians and drive a stronger economy.
            >+ *Stage 1* - Phase in LITO and LMITO
            >+ *Stage 2* - Revise tax brackets to push the 90k threshold to 120k and increase LITO and LMITO.
            >+ *Stage 3* - Revise tax brackets by removing the 37(%) Tax Bracket and changing the 32.5(%) bracket down to 30(%).
        
            The revision by the current government works under the following outcomes:
                
            > - Labor Senators support low and middle income tax relief.
            > - Labor Senators want to ensure that a future Government can properly fund public services such as health, education and infrastructure while recognising that low and middle income households are under pressure. Labor Senators will not support unsustainable levels of tax cuts that put essential public services at risk.
            """)
            st.subheader("Suggestion:")
            st.markdown("""
            If the goal is to support the future functions of Government it would be better advised to look into the LITO and LMITO levers as they had the best impact in delievering outcomes; having more poeple pay into the tax system.
                
            With the current proposal, the short term benefit may not help in realising better outcomes as people that are better off have more opportunities available to them in reducing thier overall tax liability.  The Tradie next door earning over 190k is more incentivised into organising a business structure now because they will have notionally saved 19(%) off thier tax bill.
            """)

if __name__ == "__main__":
    main()
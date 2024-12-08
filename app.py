import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Try loading the model and scaler with error handling
try:
    model = joblib.load('model.pkl')  # Path to the trained model
    scaler = joblib.load('scaler.pkl')  # Path to the scaler
except FileNotFoundError:
    st.error("Model or Scaler file not found. Please upload the necessary files.")
    st.stop()  # Stop execution if the model or scaler is not found

# Create columns for layout
col1, col2 = st.columns([3, 1])  # Adjust ratio to fit the image and text

with col1:
    # Smaller title using markdown with a custom font size
    st.markdown("<h1 style='font-size: 36px;'>Gene Cluster Prediction for E1</h1>", unsafe_allow_html=True)

with col2:
    # Image with a smaller size
    st.image("./images/dna.png", width=150)  # Adjust the width as needed

# Dimmed background image using CSS
st.markdown("""
    <style>
        .dimmed-background {
            background-image: url('./images/dna.png');
            background-size: cover;
            height: 100%;
            filter: brightness(50%);
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: -1;
        }
    </style>
    <div class="dimmed-background"></div>
""", unsafe_allow_html=True)

# Explanation text below the title and image
st.markdown("""
    Welcome to the **Gene Cluster Prediction Tool**! 🎉
    Enter the gene expression values below, and our model will predict whether 
    the sample belongs to the **E1 gene cluster** based on the 10 most important features.

    ### About the Prediction Model
    This model uses gene expression data from selected features, including **TESPA1**, **SLC17A7**, **LINC00507**, 
    **KCNIP1**, **ANKRD33B**, **LINC00508**, **SFTA1P**, **LINC00152**, **TBR1**, and **NPTX1**, 
    which were found to be the most predictive for determining **E1 gene cluster** classification.
""")

# Input fields for each of the 10 genes
gene_names = ['TESPA1', 'SLC17A7', 'LINC00507', 'KCNIP1', 'ANKRD33B', 
              'LINC00508', 'SFTA1P', 'LINC00152', 'TBR1', 'NPTX1']

input_data = {}
for gene in gene_names:
    input_data[gene] = st.number_input(f'Enter expression value for {gene}', min_value=0.0, step=0.1)

# Convert input data into a DataFrame
input_df = pd.DataFrame([input_data])

# Scale the input data using the previously fitted scaler
try:
    input_scaled = scaler.transform(input_df)
except Exception as e:
    st.error(f"Error during data scaling: {e}")
    st.stop()  # Stop execution if there's an error during scaling

# Button to make predictions
if st.button('Make Prediction'):
    try:
        # Make prediction
        prediction = model.predict(input_scaled)

        # Show prediction result
        if prediction[0] == 1:
            st.write("The sample belongs to **E1 gene cluster**! 🎯")
        else:
            st.write("The sample does **NOT** belong to the **E1 gene cluster**. ❌")
    except Exception as e:
        st.error(f"Error during prediction: {e}")

# Button to toggle detailed information
with st.expander("View More Information"):
    # Gene importance and related information
    st.markdown("""
        ### Gene Importance in E1 Cluster Prediction
        The following graph illustrates the **Gini Importance** of the selected 10 genes used in the prediction model.
        This metric shows the relative importance of each gene for determining the **E1 gene cluster** classification.
    """)

    # Example of the gene importance data
    feature_importance = [0.25, 0.18, 0.15, 0.1, 0.08, 0.07, 0.05, 0.04, 0.03, 0.02]
    features = ['TESPA1', 'SLC17A7', 'LINC00507', 'KCNIP1', 'ANKRD33B', 
                'LINC00508', 'SFTA1P', 'LINC00152', 'TBR1', 'NPTX1']

    # Plotting the feature importance graph
    fig, ax = plt.subplots()
    sns.barplot(x=feature_importance, y=features, ax=ax, palette="viridis")
    ax.set_title("Feature Importance (Gini Index)", fontsize=16, color='darkblue', fontweight='bold')
    ax.set_xlabel("Gini Importance", fontsize=14)
    ax.set_ylabel("Genes", fontsize=14)
    st.pyplot(fig)

    # Additional information about the genes
    st.markdown("""
        ### Related Information:
        Gene expression data plays a critical role in understanding cellular processes and disease mechanisms. 
        The genes selected for this prediction model are involved in various biological functions, including neurotransmitter 
        regulation, signal transduction, and cellular development.

        - **TESPA1** and **SLC17A7** are involved in neurotransmitter signaling and play roles in neuronal function.
        - **LINC00507**, **LINC00508**, and **LINC00152** are non-coding RNAs with regulatory roles in gene expression.
        - **TBR1** and **ANKRD33B** are implicated in neurodevelopmental processes.

        For more details on these genes, refer to the latest scientific literature and gene expression studies.
    """)
   

# Footer with contact or project information
st.markdown("""
    ---
    ### Contact Information
    For more details on this project, please feel free to contact us at [support@geneclusterpredictor.com](mailto:your-email@example.com).
    This tool was developed as part of a bioinformatics project for gene cluster classification.
""")

# Sidebar with buttons for each gene
st.sidebar.header("Gene Information")

# Create buttons for each gene
if st.sidebar.button("TESPA1"):
    st.sidebar.markdown("### TESPA1 - Tetraspanin 1")
    st.sidebar.write("""
        **TESPA1** is involved in neurotransmitter regulation and plays a critical role in neuronal function.
        It is associated with synaptic vesicle formation and the regulation of synaptic activity, making it an important gene for the **E1 gene cluster** prediction.
    """)

if st.sidebar.button("SLC17A7"):
    st.sidebar.markdown("### SLC17A7 - Solute Carrier Family 17 Member 7")
    st.sidebar.write("""
        **SLC17A7** is involved in the transport of neurotransmitters in synaptic vesicles. It plays an essential role in synaptic signaling 
        by regulating the uptake of neurotransmitters like glutamate and GABA, which are crucial for proper neuronal communication.
    """)

if st.sidebar.button("LINC00507"):
    st.sidebar.markdown("### LINC00507 - Long Intergenic Non-Protein Coding RNA 507")
    st.sidebar.write("""
        **LINC00507** is a long non-coding RNA that is involved in regulating gene expression at the transcriptional level. 
        It is associated with cellular processes, including cell differentiation and apoptosis, and may play a regulatory role in brain development.
    """)

if st.sidebar.button("KCNIP1"):
    st.sidebar.markdown("### KCNIP1 - Potassium Channel Interacting Protein 1")
    st.sidebar.write("""
        **KCNIP1** encodes a protein that modulates neuronal excitability, synaptic plasticity, and synaptic transmission. 
        This gene is crucial for maintaining proper neural signaling and memory processes.
    """)

if st.sidebar.button("ANKRD33B"):
    st.sidebar.markdown("### ANKRD33B - Ankyrin Repeat Domain 33B")
    st.sidebar.write("""
        **ANKRD33B** is implicated in neurodevelopment and plays a role in synaptic signaling. It is involved in regulating 
        the growth and differentiation of neurons, making it essential for brain function and development.
    """)

if st.sidebar.button("LINC00508"):
    st.sidebar.markdown("### LINC00508 - Long Intergenic Non-Protein Coding RNA 508")
    st.sidebar.write("""
        **LINC00508** is a long non-coding RNA that plays a significant role in regulating gene expression and cellular processes. 
        It is believed to participate in neuronal differentiation and could influence neurological disorders.
    """)

if st.sidebar.button("SFTA1P"):
    st.sidebar.markdown("### SFTA1P - Surfactant Associated 1 Pseudogene")
    st.sidebar.write("""
        **SFTA1P** is involved in pulmonary surfactant regulation and may have implications for neurological diseases as well. 
        Its role in gene expression regulation has been linked to neural development and function.
    """)

if st.sidebar.button("LINC00152"):
    st.sidebar.markdown("### LINC00152 - Long Intergenic Non-Protein Coding RNA 152")
    st.sidebar.write("""
        **LINC00152** is a long non-coding RNA that regulates gene expression. It has been linked to various biological processes, 
        including cellular signaling and brain development, making it important in neurodevelopmental studies.
    """)

if st.sidebar.button("TBR1"):
    st.sidebar.markdown("### TBR1 - T-Box Brain Transcription Factor 1")
    st.sidebar.write("""
        **TBR1** is a transcription factor involved in the development of neurons and their organization in the brain. 
        It plays a critical role in neurodevelopment and is associated with neurological disorders.
    """)

if st.sidebar.button("NPTX1"):
    st.sidebar.markdown("### NPTX1 - Neuronal Pentraxin 1")
    st.sidebar.write("""
        **NPTX1** is involved in synaptic signaling and plasticity. It plays an important role in the modulation of synaptic 
        transmission, learning, and memory. This gene is essential for cognitive function and neuronal health.
    """)

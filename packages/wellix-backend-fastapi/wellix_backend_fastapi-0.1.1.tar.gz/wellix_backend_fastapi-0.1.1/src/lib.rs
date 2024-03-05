use pyo3::{prelude::*, types::PyDict};

#[pyfunction]
fn check_drug_interaction(
    drug1: &str,
    drug2: &str,
    drug_interactions: Vec<PyObject>,
) -> Option<PyObject> {
    // Acquire the Python Global Interpreter Lock (GIL) to safely work with Python objects
    Python::with_gil(|py| {
        // Iterate through each interaction object in the list of drug interactions
        for interaction in drug_interactions {
            // Attempt to downcast the current interaction object to a Python dictionary
            if let Ok(interaction_dict) = interaction.downcast::<PyDict>(py) {
                // Extract the list of drugs involved in the interaction from the dictionary
                let drugs = interaction_dict
                    .get_item("interaction")? // Get the value associated with the key "interaction"
                    .extract::<Vec<String>>() // Extract the value as a Vec<String>
                    .expect("failed to downcast"); // Return None if extraction fails

                // Convert the input drug names to lowercase for case-insensitive comparison
                let (drug1, drug2) = (drug1.to_lowercase(), drug2.to_lowercase());

                // Compare the drugs involved in the interaction with the input drug names
                // If either order of the drugs matches the input, return the interaction object
                if (drugs[0].to_lowercase() == drug1 && drugs[1].to_lowercase() == drug2)
                    || (drugs[0].to_lowercase() == drug2 && drugs[1].to_lowercase() == drug1)
                {
                    return Some(interaction);
                }
            }
        }
        // Return None if no matching interaction is found
        None
    })
}

#[pymodule]
fn wellix_backend_fastapi(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(check_drug_interaction, m)?)?;
    Ok(())
}

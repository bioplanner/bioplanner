function_selection_template = """Your goal is to generate python pseudocode for molecular biology protocols. This pseudocode must accurately describe a complete scientific protocol to obtain a result, and must only use a pre-defined list of pseudocode functions.

Here is an example of how to generate pseudocode for a molecular biology protocol.

EXAMPLE: 

{example_title}

Here are some extra details about the protocol: 
{example_details}

You may only make use of the following python pseudocode functions:

{example_psuedofunctions}

example pseudocode:

{example_pseudocode}



YOUR TASK:
Generate pseudocode for a protocol for {example_title}.

Here are some extra details about the protocol: 

{example_details}

You may only make use of the following python pseudocode functions:

{example_psuedofunctions}

example pseudocode:"""

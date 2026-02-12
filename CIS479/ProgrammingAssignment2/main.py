import random
import sys

CPTs = {
    # givens
    'B': 0.001,
    'E': 0.002,
    'A': {
        ('t', 't'): 0.95,
        ('t', 'f'): 0.94,
        ('f', 't'): 0.29,
        ('f', 'f'): 0.001,
    },
    'J': {
        ('t',): 0.90,
        ('f',): 0.05,
    },
    'M': {
        ('t',): 0.70,
        ('f',): 0.01,
    }
}
TOPOLOGICAL_ORDER = ['B', 'E', 'A', 'J', 'M']

# The structure that defines the parents of each node
NETWORK_STRUCTURE = {
    #P(B), P(A|B,E) type thing. if its in the brackets its given
    'B': [],
    'E': [],
    'A': ['B', 'E'],
    'J': ['A'],
    'M': ['A']
}

# Experiment Parameters 
SAMPLES = [10, 50, 100, 200, 500, 1000, 10000] # desired running states
NUM_RUNS_PER_SAMPLE_SIZE = 10 

def get_prob_true(node, assignment):
    parents = NETWORK_STRUCTURE[node] #parents are existing nodes. initiative
    
    if parents:
        parent_construction = tuple(assignment[p] for p in parents) #assigns which t or f im using in A|B,E for situation
        prob_true = CPTs[node][parent_construction]
        #CPTs[node] grabs the node, parent_construction assigns the t/f to the node.
    else:
        prob_true = CPTs[node]#P(b), like there is no given in it so just node
        
    return prob_true#give back example of P(A|B,E)

def prior_sample():
    assignment = {} 
    
    for node in TOPOLOGICAL_ORDER:
        prob_true = get_prob_true(node, assignment)#grab P(B), then P(E),then P(A|B,E), then P(A|B,E')...
       #The below if statement makes it so that every true value is less than the stuff in the figure.
       #so if i ran infinite samples, i would again have 94% are true, instead of arbitrary 97% or something.
        if random.random() < prob_true:#random function
            sampled_value = 't'
        else:
            sampled_value = 'f'
            
        assignment[node] = sampled_value#
        
    return assignment

def exact_inference(evidence, query_vars):

    def calculate_probability_of_assignment(target_assignment):

        
        def recursive_enumerate(vars_list, current_assignment):
            if not vars_list:
                return 1.0
            
            # Take the first variable from the list
            Y = vars_list[0]
            rest = vars_list[1:]#*THE* rest
            #[Y,Rest_0,Rest_1,...] for example
            
           #function
            prob_true = get_prob_true(Y, current_assignment)
            
           #This, and its accompanying else statement, are what actually make probability through b-m.
            if Y in target_assignment:
                val = target_assignment[Y]
      
                current_assignment[Y] = val
                
                if val == 't':
                    prob = prob_true
                else:
                    prob = 1.0 - prob_true
                    #finish B, go to E, finish E, go to A... doing this turns Y into E, and Rest into [a,j,m]
                return prob * recursive_enumerate(rest, current_assignment)
                
            else:
                current_assignment[Y] = 't'
                term_t = prob_true * recursive_enumerate(rest, current_assignment)
                
                # Case 2: Assume Y is False
                current_assignment[Y] = 'f'
                term_f = (1.0 - prob_true) * recursive_enumerate(rest, current_assignment)
                
                return term_t + term_f

        return recursive_enumerate(TOPOLOGICAL_ORDER, {})#all the probabilities. basically this is the last call in rec enum.

    # 1. Calculate Numerator. done by grabbing it.
    query_and_evidence = evidence.copy()
    for var in query_vars:
        query_and_evidence[var] = 't' # Queries are for True
        
    prob_query_and_evidence = calculate_probability_of_assignment(query_and_evidence)
    
    # 2. Calculate Denominator. Done  by grabbing it.
    prob_evidence = calculate_probability_of_assignment(evidence)
    
    # 3. Final Calculation: P(Q and Evidence) / P(Evidence)=P(Q|Evidence)
    if prob_evidence == 0:#just incase
        return 0.0
    
    return prob_query_and_evidence / prob_evidence #getting P(Q|E)

# C3. Prior Sampling Inference 
#calculates P(Query), or the LHS of P(A|b,e), the A part

def prior_sampling_inference(evidence, query_vars, num_samples):
 
    count_matching_Q = 0
    
    for _ in range(num_samples):
        #sample=new probabilities but same name. basically this is when the new stuff is messed with
        sample = prior_sample() 
        
        # Check if sample satisfies the query (Q)
        query_matches = all(sample[var] == 't' for var in query_vars)
        #get all new_prob<orig_prob. basically get the stuff that we want
        
        if query_matches:
            count_matching_Q += 1#used for indexing

    return count_matching_Q / num_samples if num_samples > 0 else 0.0 #basically, take amt(true)/amt(total)


# C4. Rejection Sampling Inference (R)
#same function as prior sampling inference but for evidence
def rejection_sampling_inference(evidence, query_vars, num_samples):
    count_matching_Q_and_E = 0
    total_matching_E = 0
    
    for _ in range(num_samples):#run "num_samples" times
        sample = prior_sample() 
        
        # Check if the sample is consistent with the evidence (E)
        evidence_matches = all(sample[var] == val for var, val in evidence.items())
        #same fucntion as query_matches no difference
        if evidence_matches:
            total_matching_E += 1
            
            # Check if the sample also satisfies the query (Q)
            query_matches = all(sample[var] == 't' for var in query_vars)
            
            if query_matches:
                count_matching_Q_and_E += 1

    if total_matching_E == 0:
        return 0.0
    return count_matching_Q_and_E / total_matching_E


# C5. Likelihood Weighting Inference (LW)

def likelihood_weighting_inference(evidence, query_vars, num_samples):
 
    weighted_count_Q = 0.0
    total_weight = 0.0
    
    for _ in range(num_samples):
        # 1. Initialize assignment and weight
        assignment = {}#initialize
        weight = 1.0
        
        # 2. Loop through variables in topological order
        for node in TOPOLOGICAL_ORDER:
            parents = NETWORK_STRUCTURE[node]#this is just the A|b,e stuff again, the B,E side specifically
            # Use assignment to determine parent values for CPT lookup
            
            if node in evidence:
                # Case 1: Variable is evidence (E)
                val = evidence[node]
                assignment[node] = val
                
                # Get P(Node=val | Parents) and update weight
                prob_true = get_prob_true(node, assignment) 
                
                if val == 't':
                    prob_conditional = prob_true
                else: # val == 'f'
                    prob_conditional = 1.0 - prob_true
                    
                weight *= prob_conditional#because weight=1, this just means that we get prob_cond again. but this is done because i want weight to update per run. if i had just prob_cond it'd require a list
            
            else:
                # Case 2: Variable is not evidence - Sample value
                prob_true = get_prob_true(node, assignment)
                if random.random() < prob_true:
                    assignment[node] = 't'
                else:
                    assignment[node] = 'f'
        
        # 3. Check if the generated sample matches the query (Q)
        query_matches = all(assignment[var] == 't' for var in query_vars)
        
        # 4. Update counts
        if query_matches:
            weighted_count_Q += weight #prob_cond_1+prob_cond_2+... when the cond_prob is true.
        
        total_weight += weight#prob_cond_1+prob_cond_2, no matter what

    if total_weight == 0.0:
        return 0.0
    return weighted_count_Q / total_weight#example: prob_cond_1-prob_cond_100 divided by prob_cond_1-prob_cond_10000. numerator will have less terms 


# C6. Input/Output Handlers 

def parse_input_string(s):
    """
    Parses input like:  [<A,t><B,f>][J, M]
    Returns:
       evidence = {'A':'t', 'B':'f'}
       query_vars = ['J','M']
    """
    s = s.strip()

    # Split into evidence part and query part
    try:
        evidence_str = s[s.index('[')+1 : s.index(']')]
        query_str = s[s.rindex('[')+1 : s.rindex(']')]
    except:
        raise ValueError("Input string not in correct format.")

    # Parse evidence 
    evidence = {}
    import re
    pattern = r"<([A-Z]),\s*([tf])>"
    matches = re.findall(pattern, evidence_str)
    for var, val in matches:
        evidence[var] = val

    # Parse query variables 
    query_vars = re.split(r"[,\s]+", query_str.strip())  # split on commas or spaces
    query_vars = [q.strip() for q in query_vars if q]    # remove empty strings

    return evidence, query_vars

def format_output(query_vars, probability_estimate):
    """
    Formats a single JOINT probability as:
    [<B, J, 0.00000301>]
    """
    vars_part = ", ".join(query_vars)  # space after comma
    return f"[<{vars_part}, {probability_estimate:.8f}>]"  # 8 decimals


# Change the function signature to accept report_file
def print_report_table(query_name, results, exact_result, report_file): 
    """
    Writes the collected data in the required table format to the provided file object.
    """
    # Use file.write() instead of print()
    report_file.write(f"\n-----------------------------------------------------------------\n")
    report_file.write(f"REPORT TABLE GENERATED FOR: {query_name}\n")
    report_file.write("-----------------------------------------------------------------\n")

    
    # Print Header
    header = f"{'Samples Num':<12} | {'Prior Sampling':<15} | {'Rejection':<12} | {'LW':<12}\n"
    report_file.write(header)
    report_file.write("-" * 60 + "\n")
    
    # Print Sampling Results
    for N in SAMPLES:
        data = results[N]
        line = f"{N:<12} | {data['Prior']:<15.8f} | {data['Rejection']:<12.8f} | {data['LW']:<12.8f}\n"
        report_file.write(line)

    # Print Exact Result (last row)
    report_file.write("-" * 60 + "\n")
    exact_line = f"{'Exact':<12} | {'-':<15} | {'-':<12} | {exact_result:<12.8f}\n"
    report_file.write(exact_line)


# Change the function signature to accept report_file
def run_experiments_for_query(query_case, report_file): 
    """
    Runs all sampling algorithms for a specific query case across all sample sizes, 
    averaging the results 10 times.
    """
    evidence = query_case['evidence']
    query_vars = query_case['query_vars']
    
    results = {} 

    # 1. Calculate Exact Inference Result (Done only once) 
    exact_result = exact_inference(evidence, query_vars) 

    # 2. Iterate through all required sample sizes 
    for N in SAMPLES:
        # ... (keep the rest of the loop for running algorithms 10 times) ...
        prior_runs = []
        rejection_runs = []
        lw_runs = []
        
        for _ in range(NUM_RUNS_PER_SAMPLE_SIZE):
            # Run your three implemented sampling algorithms
            P = prior_sampling_inference(evidence, query_vars, N)#THIS is the main line where everything is actually ran
            R = rejection_sampling_inference(evidence, query_vars, N)
            L = likelihood_weighting_inference(evidence, query_vars, N)

            prior_runs.append(P)#counting
            rejection_runs.append(R)
            lw_runs.append(L)

        # 4. Calculate the average probability over the 10 runs
        avg_prior = sum(prior_runs) / NUM_RUNS_PER_SAMPLE_SIZE #89/100
        avg_rejection = sum(rejection_runs) / NUM_RUNS_PER_SAMPLE_SIZE
        avg_lw = sum(lw_runs) / NUM_RUNS_PER_SAMPLE_SIZE
        
        results[N] = {
            'Prior': avg_prior,
            'Rejection': avg_rejection,
            'LW': avg_lw
        }

    #  5. Call the printing function, passing the file object
    print_report_table(query_case['name'], results, exact_result, report_file)

REPORT_FILENAME = "bayes_net_experiment_report.txt"

def user_input_to_query(user_input):
    evidence, query_vars = parse_input_string(user_input)
    return {
        'name': f"User Query: {', '.join(query_vars)} | Evidence: {evidence}",
        'evidence': evidence,
        'query_vars': query_vars
    }

#runs the code and pastes it out
def run_all_experiments(user_query=None):
    try:
        with open(REPORT_FILENAME, 'w') as report_file:

            report_file.write("-----------------------------------------------------------------\n")
            report_file.write("Starting experiments to generate report tables...\n")
            report_file.write("-----------------------------------------------------------------\n")

            queries_to_run = [user_query]

            for i, query in enumerate(queries_to_run):
                report_file.write(f"\n--- Running Query {i+1}: {query['name']} ---\n")
                run_experiments_for_query(query, report_file)

            report_file.write("\nAll experiments complete.\n")

        print(f"\nSUCCESS! Tables have been generated and saved to: {REPORT_FILENAME}")

    except IOError:
        print(f"\nERROR: Could not write to file {REPORT_FILENAME}. Check permissions.")


if __name__ == "__main__":
    user_query = None

    if len(sys.argv) > 1:
        # User provided query as command-line argument
        input_string = sys.argv[1]
    else:
        # No argument: prompt the user for input
        print("Please enter a query and evidence in the format: [<Var1,t><Var2,f>][QueryVar1,QueryVar2]")
        input_string = input("Input: ").strip()

    # Parse the input string
    evidence, query_vars = parse_input_string(input_string)

    # Perform exact inference and print in terminal
    exact_prob = exact_inference(evidence, query_vars)
    print(format_output(query_vars, exact_prob))

    # Create a query dictionary for experiments
    user_query = {
        'name': f"User Query: {input_string}",
        'evidence': evidence,
        'query_vars': query_vars
    }

    # Run experiments and save report
    run_all_experiments(user_query)





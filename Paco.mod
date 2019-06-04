/*********************************************
 * OPL 12.6.0.0 Model
 * Authors: Amalia and Sergio
 *********************************************/

int nProviders=...;
int workers=...;
range P=1..nProviders;

// Available workers per provider
int available_workers[p in P]=...;

// Cost of hiring at least 1 worker from provider p
int cost_contract[p in P]=...;

// Country of the workers from provider p 
int country[p in P]=...;

// Price per worker of provider p.
int cost_worker[p in P]=...;


// Costs of the taxes for hiring people from
// other countries.

// Cost of the first 5 workers
int cost_1 = 2;

// Cost of the next 5 workers
int cost_2 = 10;

// Cost of the remaining workers
int cost_3 = 20;

// Whether two providers belong to the same country or not
int same_country[p1 in P, p2 in P];

// Number of workers from provider p that are hired.
dvar int hired_base[p in P];
dvar int hired_extra[p in P];

// Indicator variables to check whether we hired all,
// half or none of the workers from provider p.
dvar boolean all_hired[p in P];
dvar boolean half_hired[p in P];
dvar boolean none_hired[p in P];

// Paco dismisses the two last dvars and uses just a
// single one to check if some of the workers from
// provider p are hired
dvar boolean some_hired[p in P];

// Number of people hired belonging to the
// corresponding tax bracket.
dvar boolean hired_1[p in P];
dvar boolean hired_2[p in P];
dvar boolean hired_3[p in P];


// PREPROCESSING
execute {
  for ( var i = 1; i <= nProviders; i++)
  	for ( var j = 1; j <= nProviders; j++){
  		if(country[i] == country[j]){
    		same_country[i][j] = 1;
    	}    		
   }    	
}
;

minimize
  sum(p in P)
	((cost_contract[p] * some_hired[p]) +
		cost_worker[p] * (hired_base[p] + hired_extra[p]) +
		hired_1[p] * cost_1 + hired_2[p] * cost_2 + hired_3[p] * cost_3);

subject to {
	
	// Constraint 1 --> Not getting the idea of the summation
	forall(p in P)
	  sum(p in P) hired_base[p] <= some_hired[p] * available_workers[p];
	  
	// Constraint 2 --> The number of hired workers from any provider
	// has to be lower than or equal the number of available workers.
	forall(p in P)
	  all_hired[p] * available_workers[p] >= hired_base[p];
	
	// Constraint 3 --> The number of extra hired workers from any provider
	// has to be lower than or equal the number of available workers.
	forall(p in P)
	  hired_extra[p] <= all_hired[p] * available_workers[p];
	  
	// Constraint 4 --> With this constraint we ensure that we only hire
	// either none workers from provider p, half of them or all
	forall(p in P)
	  available_workers[p] / 2 * (some_hired[p] + all_hired[p]) == hired_base[p];
	
	// Constraint 5 --> The number of hired workers from provider p
	// have to be at most 5.   
	forall(p in P)
	  hired_1[p] <= 5;
	
	// Constraint 6 --> The number of hired workers from tax bracket 2
	// from provider p have to be at most 5.
	forall(p in P)
	  hired_2[p] <= 5;
	  
	// Constraint 7 --> ?? 
	forall(p1 in P, p2 in P: p1!=p2)
	  some_hired[p1] + some_hired[p2] + same_country[p1, p2] <= 3;
	  
	// Constraint 8 --> The final number of hired workers has to be
	// exactly the same as the number of workers we wanted to hire.
	sum(p in P) (hired_base[p] + hired_extra[p]) == workers;
}
 
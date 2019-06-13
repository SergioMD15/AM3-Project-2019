/*********************************************
 * OPL 12.8.0.0 Model
 * Author: amalia & sergio
 *********************************************/
//
// Ιnput data
//
int wr=...;
int nProviders=...;
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
int cost_1 = ...;
// Cost of the next 5 workers
int cost_2 = ...;
// Cost of the remaining workers
int cost_3 = ...;

// 
// Decision Variables
//
// # of people hired from base batch
dvar int hired_base[p in P];
// # of people hired from extra batch
dvar int hired_extra[p in P];
// 1 if any employee of provider p have been hired
dvar boolean some_hired[p in P];
// 1 if all workers from provider p have been hired
dvar boolean all_hired[p in P];
// # of people hired that belong to the 1st, 2nd and 3rd tax bracket respectively
dvar int hired_1[p in P];
dvar int hired_2[p in P];
dvar int hired_3[p in P];

// Whether two providers belong to the same country or not
int same_country[p1 in P, p2 in P];

dvar int z;

// PREPROCESSING
execute {
  for ( var i = 1; i <= nProviders; i++){
  	for ( var j = 1; j <= nProviders; j++){
  		if(i != j && country[i] == country[j]){
    		same_country[i][j] = 1;
    	}    		
	}
  }	
}
;

// objective function
minimize z;

//constraints
subject to{

	 // set z
	 z == sum(p in P) (cost_contract[p]*some_hired[p] + cost_worker[p]*(hired_base[p] + hired_extra[p])
	  + hired_1[p]*cost_1 + hired_2[p] * cost_2 + hired_3[p]*cost_3);
	  
	// Constraint 1
	// hire exactly the required number of workers wr
	sum(p in P) (hired_base[p]+hired_extra[p]) == wr;
	
	
	// Constraint 2
	forall(p in P) hired_base[p] <= some_hired[p] * available_workers[p];
	  
        // Constraint 3
	forall(p in P) all_hired[p] * available_workers[p] <= hired_base[p];
	
	// Constraint 4 
	// if we hire all workers from provider p, we can hire up to same number of extra
	forall(p in P) hired_extra[p] <= all_hired[p] * available_workers[p];
	
	// Constraint 5
	// if we hire from the provider p, hire either half or all
	forall(p in P) available_workers[p]/2 * (some_hired[p] + all_hired[p]) == hired_base[p];
	
	// Constraint 6
	forall(p in P) hired_1[p] + hired_2[p] + hired_3[p] == hired_base[p];
	
	// Constraint 7
	// hired workers belonging to the 1st bracket can be at most 5
	forall(p in P) 0 <= hired_1[p] <= 5;
	
	// Constraint 8 
	// hired workers belonging to the 2nd bracket can be at most 5
	forall(p in P) 0 <= hired_2[p] <= 5;
	
	// Constraint 9
	// the company cannot hire two providers from the same country
	forall(p1 in P, p2 in P: p1 != p2) some_hired[p1] + all_hired[p2] + same_country[p1][p2] <= 2;
	
	
	// some extras, without these two, it returns negative results (?!)
	forall(p in P)
	  hired_extra[p] >= 0;
	
	forall(p in P)
	  hired_3[p] >= 0;
}

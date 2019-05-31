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

// Number of people hired belonging to the
// corresponding tax bracket.
dvar boolean hired_1[p in P];
dvar boolean hired_2[p in P];
dvar boolean hired_3[p in P];
dvar int z;


// PREPROCESSING
execute {
  for ( var i = 1; i <= nProviders; i++){
  	for ( var j = 1; j <= nProviders; j++){
  		if(i !=j && country[i] == country[j]){
    		same_country[i][j] = 1;
    	}    		
	}
  }	
}
;

minimize
  z;

subject to {

	z == sum(p in P)
		(cost_contract[p] * (1 - none_hired[p]) +
			cost_worker[p] * (hired_base[p] + hired_extra[p])
			+ cost_1 * hired_1[p] + cost_2 * hired_2[p] + cost_3 * hired_3[p]);
	  
	// CONSTRAINT 1
	// We hire either all or less providers.
	forall(p in P)
	  all_hired[p] * available_workers[p] <= hired_base[p];
	  
	// CONSTRAINT 2
	// If we hire some providers, we can hire them all, or half of them.
	forall(p in P)
	  hired_base[p] == available_workers[p] * all_hired[p] + available_workers[p]/2 * half_hired[p]; 
 	
 	// CONSTRAINT 3
 	// Half, all and none values are excluding i.e. if one of them
 	// is true, the other ones are false.
 	forall(p in P)
 	  all_hired[p] + half_hired[p] + none_hired[p] == 1;
	  
	  
	// CONSTRAINT 4
	// If we hire some providers from two different providers
	// they have to be from different countries.
	forall(p1 in P, p2 in P: p1!=p2)
	  2 - (none_hired[p1] + none_hired[p2] + same_country[p1, p2]) <= 2;
	  
	// CONSTRAINT 5
	// The number of total providers hired in the end has to be
	// the same as the initial amount received as an input.
	sum(p in P) (hired_base[p] + hired_extra[p]) == workers;
	
	forall(p in P) hired_extra[p] >= 0;
	
	// CONSTRAINT 6 
	// The number of hired workers from tax bracket 1 from provider p
	// has to be at most 5.
	forall(p in P)
	  hired_1[p] <= 5;
	  
	// CONSTRAINT 7
	// The number of hired workers from tax bracket 2 from provider p
	// has to be at most 5.
	forall(p in P)
	  hired_2[p] <= 5;
	  
	// CONSTRAINT 8
	// The number of extra hired workers from any provider has to be
	// lower than or equal the number of available workers.
	forall(p in P)
	  hired_extra[p] <= all_hired[p] * available_workers[p];
	  
	// CONSTRAINT 9
	// The sum of the workers hired from a provider p in the different
	// tax brackets has to be equal to the extra workers hired. 
	forall(p in P)
	  hired_1[p] + hired_2[p] + hired_3[p] == hired_extra[p];
}
 
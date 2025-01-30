
SPORADIC_ORDERS = {'M11' : {2:4, 3:2, 5:1, 11:1},
                   'M12' : {2:6, 3:3, 5:1, 11:1},
                   'M22' : {2:7, 3:2, 5:1, 7:1, 11:1},
                   'M23' : {2:7, 3:2, 5:1, 7:1, 11:1, 23:1},
                   'M24' : {2:10, 3:3, 5:1, 7:1, 11:1, 23:1},
                   'J1' : {2:3, 3:1, 5:1, 7:1, 11:1, 19:1},
                   'J2' : {2:7, 3:3, 5:2, 7:1},
                   'J3' : {2:7, 3:5, 5:1, 17:1, 19:1},
                   'J4' : {2:21, 3:3, 5:1, 7:1, 11:3, 23:1, 29:1, 31:1, 37:1, 43:1},
                   'Co1' : {2:21, 3:9, 5:4, 7:2, 11:1, 13:1, 23:1},
                   'Co2' : {2: 18, 3: 6, 5: 3, 7: 1, 11: 1, 23: 1},
                   'Co3' : {2: 10, 3: 7, 5: 3, 7: 1, 11: 1, 23: 1},
                   'Fi22' : {2: 17, 3: 9, 5: 2, 7: 1, 11: 1, 13: 1},
                   'Fi23' : {2: 18, 3: 13, 5: 2, 7: 1, 11: 1, 13: 1, 17: 1, 23: 1},
                   'Fi24\'' : {2: 21, 3: 16, 5: 2, 7: 3, 11: 1, 13: 1, 17: 1, 23: 1, 29: 1},
                   'HS' : {2: 9, 3: 2, 5: 3, 7: 1, 11: 1},
                   'McL' : {2: 7, 3: 6, 5: 3, 7: 1, 11: 1},
                   'He' : {2: 10, 3: 3, 5: 2, 7: 3, 17: 1},
                   'Ru' : {2: 14, 3: 3, 5: 3, 7: 1, 13: 1, 29: 1},
                   'Suz': {2: 13, 3: 7, 5: 2, 7: 1, 11: 1, 13: 1},
                   'ON' : {2: 9, 3: 4, 5: 1, 7: 3, 11: 1, 19: 1, 31: 1},
                   'HN' : {2: 14, 3: 6, 5: 6, 7: 1, 11: 1, 19: 1},
                   'Ly' : {2: 8, 3: 7, 5: 6, 7: 1, 11: 1, 31: 1, 37: 1, 67: 1},
                   'Th' : {2: 15, 3: 10, 5: 3, 7: 2, 13: 1, 19: 1, 31: 1},
                   'B' : {2: 41, 3: 13, 5: 6, 7: 2, 11: 1, 13: 1, 17: 1, 19: 1, 23: 1, 31: 1, 47: 1},
                   'M' : {2: 46, 3: 20, 5: 9, 7: 6, 11: 2, 13: 3, 17: 1, 19: 1, 23: 1, 29: 1, 31: 1, 41: 1, 47: 1, 59: 1, 71: 1}
                   }

SPORADIC_MULTIPLIERS = {'M11' : 1, 'M12' : 2, 'M22' : 12,'M23' : 1,'M24' : 1,'J1' : 1,'J2' : 2,'J3' : 3,'J4' : 1,'Co1' : 2,'Co2' : 1,
                        'Co3' : 1,'Fi22' : 6,'Fi23' : 1,'Fi24\'' : 3,'HS' : 2,'McL' : 3,'He' : 1,'Ru' : 2,'Suz': 6,'ON' : 3,'HN' : 1,
                        'Ly' : 1,'Th' : 1,'B' : 2,'M' : 1}

TITS_ORDER = {2: 11, 3: 3, 5: 2, 13: 1}

CHEVALLEY_E6_POWER_INDICES = [2,5,6,8,9,12]
CHEVALLEY_E7_POWER_INDICES = [2,6,8,10,12,14,18]
CHEVALLEY_E8_POWER_INDICES = [2,8,12,14,18,20,24,30]
CHEVALLEY_F4_POWER_INDICES = [2,6,8,12]
CHEVALLEY_G2_POWER_INDICES = [2,6]
STEINBERG_2E6_POWER_INDICES = [2,5,6,8,9,12]


class SimpleGroupsOrder:
    def __init__(self, order=2, multipliers = False):
        self.order = dict()
        self.primes = set()
        self.multipliers = multipliers
        self.current_group_list = []
        self.current_group_multiplier_list = dict()
        self.set_order(order)
    
    def set_order(self, order):
        if type(order) == type(dict()):
            self.order = order
        else:
            self.order = dict(factor(order))
        self.primes = set(self.order)
        return self.order
    
    def set_multipliers(self,multipliers):
        self.multipliers = multipliers

    def reset(self, order=2, multipliers = False):
        self.__init__(order=order,multipliers=multipliers)
    
    def clear_groups(self):
        self.current_group_list = []
        self.current_group_multiplier_list = dict()
    
    def get_calculated_groups(self):
        if self.multipliers:
            return self.current_group_multiplier_list
        else:
            return self.current_group_list
    
    def get_all_groups(self):
        self.full_check()
        return self.get_calculated_groups()

    def __alternating_candidate__(self,points,prime):
            candidate = 0
            while points>prime-1:
                # First rough estimate for a candidate based on available points
                base_candidate_power = int(floor(log(points,prime)+1)) # log(p*k,p) = 1+log(k,p)
                # We calculate the points necessary to obtain our candidate 
                base_candidate_points = (prime**base_candidate_power-1)//(prime-1)
                # Points needed for promotion = base_candidate_power
                # First we test if we have overstimated and are not in promotion range
                # Then we test if we are in promotion range, else we promote
                if base_candidate_points - base_candidate_power > points:
                    # We are not in promotion range
                    base_candidate_power -= 1
                    points -= (prime**base_candidate_power-1)//(prime-1)
                    candidate += prime**base_candidate_power
                elif base_candidate_points > points:
                    # We are in promotion range but do not have enough to promote
                    # We add until previous to promotion and remove points
                    candidate += prime**base_candidate_power - prime
                    points = 0
                else:
                    # We promote and remove points
                    points -= base_candidate_points
                    candidate += prime**base_candidate_power
            # Extend until just befote the next multiple + excess points
            candidate += prime*points + prime-1
            return candidate

    def alternating(self):
        # Consider n>4
        n_candidates = []
        # We first check for a prime gap in self.primes
        # Generate the first len(self.primes) + 1 prime numbers
        first_primes = primes_first_n(len(self.primes)+1)
        for i in range(len(self.primes)):
            if sorted(self.primes)[i] != first_primes[i]:
                # We keep the primes before the gap
                n_candidates.append(first_primes[i]-1)
                first_primes = first_primes[:i]
                break
        # If there is no gap, we add bound and keep all available primes
        if len(first_primes)-1 == len(self.primes):
            n_candidates.append(first_primes[i+1]-1)
            first_primes = first_primes[:-1]
        # If the list does not contain 2,3,5 then there are no candidates
        if len(first_primes) < 3:
            return
        # For each prime factor and its power we calculate its maximum compatible n
        # We treat 2 slightly different since the order of A_n is n!/2, aka 2 has an extra point
        n_candidates.append(self.__alternating_candidate__(self.order[2]+1,2))
        for prime in first_primes[1:]:
            n_candidates.append(self.__alternating_candidate__(self.order[prime],prime))
        # Having obtained all compatible candidates for each power, the candidate compatible with all is the minimum
        max_n = min(n_candidates)
        # We add compatible A_n to the group list
        if self.multipliers:
            print(max_n)
            if max_n > 7:
                self.current_group_multiplier_list['A5'] = 2
                self.current_group_multiplier_list['A6'] = 6
                self.current_group_multiplier_list['A7'] = 6
                for n in range(8,max_n+1):
                    self.current_group_multiplier_list['A' + str(n)] = 2
            elif max_n == 7:                
                self.current_group_multiplier_list['A5'] = 2
                self.current_group_multiplier_list['A6'] = 6
                self.current_group_multiplier_list['A7'] = 6
            elif max_n == 6:
                self.current_group_multiplier_list['A5'] = 2
                self.current_group_multiplier_list['A6'] = 6
            elif max_n == 5:
                self.current_group_multiplier_list['A5'] = 2
        else:
            for n in range(5,max_n+1):
                self.current_group_list.append('A' + str(n))
        return n_candidates
    
    def sporadic(self):
        for group in SPORADIC_ORDERS:
            # We check if prime factors are compatible
            if set(SPORADIC_ORDERS[group]) <= self.primes:
                compatible = True
                # We check if prime order is compatible
                for prime in SPORADIC_ORDERS[group]:
                    if SPORADIC_ORDERS[group][prime] > self.order[prime]:
                        compatible = False
                        break
                if compatible and self.multipliers :
                    self.current_group_multiplier_list[group] = SPORADIC_MULTIPLIERS[group]
                elif compatible and not self.multipliers:
                    self.current_group_list.append(group)

    
    def chevalley_A(self):
        for prime in self.primes:
            # Chevalley type A groups depend on n and q=prime**k, n>0
            for k in range(1,self.order[prime]+1):
                q = prime**k
                n = 1
                # We will build the order of the product term iteratibly for each q
                product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
                # Since the order contains q**(n*(n+1)/2) we have a stopping condition to test each n
                compatible = True
                while self.order[prime] >= k*n*(n+1)/2:
                    # We build the term of the product for the current n
                    term_order = dict(factor(q**(n+1)-1))
                    # We build product order now, notice it may have primes not found in it already
                    for tprime in term_order:
                        if tprime in self.primes:
                            product_order[tprime] += term_order[tprime]
                        else:
                            product_order[tprime] = term_order[tprime]
                    # We cannot modify product_order since we may need it in next iteration
                    # so we create a relative product order to take care of the gcd term
                    relative_product_order = copy(product_order)
                    # We add 1/(gcd(n+1,q-1)), notice it divides q**2-1
                    if gcd(n+1,q-1) != 1:
                        gcd_factors = dict(factor(gcd(n+1,q-1)))
                        # gcd_factors may cancel primes not contained in self.primes, so we remove such cases
                        for gprime in gcd_factors:
                            relative_product_order[gprime] -= gcd_factors[gprime]
                        for gprime in set(relative_product_order).difference(self.primes):
                            if relative_product_order[gprime] == 0:
                                del relative_product_order[gprime]
                        
                    # We check prime factors compatibility
                    if not set(relative_product_order.keys()) <= self.primes :
                        # If they are not compatible
                        compatible = False
                    
                    # We now check prime order compatibility against the relative order
                    if compatible:
                        for pprime in product_order:
                            if relative_product_order[pprime] > self.order[pprime]:
                                compatible = False
                                break
                    # If prime orders are compatible we add the group
                    # Notice: (q,n)=(2,1) and (q,n)=(3,1) are not simple
                    if compatible and (q == 2 and n == 1) or (q == 3 and n == 1):
                        n += 1
                        continue
                    if compatible and self.multipliers:
                        if q == 4 and n == 1:
                            self.current_group_multiplier_list['L' + str(n+1) + '(' + str(q) + ')'] = 2
                        elif q == 9 and n == 1:
                            self.current_group_multiplier_list['L' + str(n+1) + '(' + str(q) + ')'] = 6
                        elif q == 2 and n == 2:
                            self.current_group_multiplier_list['L' + str(n+1) + '(' + str(q) + ')'] = 2
                        elif q == 4 and n == 2:
                            self.current_group_multiplier_list['L' + str(n+1) + '(' + str(q) + ')'] = 48
                        else:
                            self.current_group_multiplier_list['L' + str(n+1) + '(' + str(q) + ')'] = gcd(n+1,q-1)
                    elif compatible and not self.multipliers:
                        self.current_group_list.append('L' + str(n+1) + '(' + str(q) + ')')
                    # We increase n by 1
                    n += 1


    def chevalley_B_C(self):
        # Notice: if q=2**k then gcd(2,q-1)=1 so first check condition still holds
        # Chevalley type B and C groups depend on n and q=prime**k, n>1 and n>2 resp.
        # First compatibility check
        if max(self.order.values()) < 4:
            return
        # We determine compatible primes
        compatible_primes = []
        for prime in self.primes:
            if self.order[prime] >= 4:
                compatible_primes.append(prime)
        # For each compatible prime 
        for prime in compatible_primes:
            # q=p**k is compatible if self.order[prime] >= 4*k
            for k in range(1,self.order[prime]//4 + 1):
                q = prime**k
                n = 2
                # We build the product term by adding the first term
                product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
                #  Notice that if q = 2**k then gcd(2,q-1)=1, if q = p**k, p!=2 then gcd(2,q-1)=2 so
                first_term_order = dict(factor(q**2-1))
                if 2 in self.primes:
                    product_order[2] -= 1
                else:
                    if first_term_order[2] == 1:
                        del first_term_order[2]
                    else:
                        # If 2 is not a prime in self.order and is not removed then the primes of product_order don't match self.primes
                        continue
                # We check if the first terms' primes are compatible
                if set(first_term_order.keys()) <= self.primes:
                    # We merge the term order into product_order
                    for tprime in first_term_order:
                        product_order[tprime] += first_term_order[tprime]
                else:
                    # If they are not compatible we skip to next k
                    continue
                # We continue building the product term for bigger n's
                # Since the order contains q**(n**2) we have a stopping condition to test each n
                compatible = True
                while self.order[prime] >= k*n**2:
                    # We build the order of the current term
                    term_order = dict(factor(q**(2*n)-1))
                    # We check if prime factors are compatible
                    if set(term_order.keys()) <= self.primes:
                        # We merge the term order into product_order
                        for tprime in term_order:
                            product_order[tprime] += term_order[tprime]
                    else:
                        # If they are not compatible we stop
                        compatible = False
                        break
                    for pprime in product_order:
                        if product_order[pprime] > self.order[pprime]:
                            compatible = False
                            break
                    # If prime orders are compatible we add the group
                    # Notice (q,n) = (2,2) is not simple
                    if n == 2 and q == 2:
                        n += 1
                        continue
                    if compatible and self.multipliers :
                        if n == 3 and q == 2:
                            self.current_group_multiplier_list['O' + str(2*n+1) + '(' + str(q) + ')'] = 2
                        elif n == 3 and q == 3:
                            self.current_group_multiplier_list['O' + str(2*n+1) + '(' + str(q) + ')'] = 6
                        else:
                            self.current_group_multiplier_list['O' + str(2*n+1) + '(' + str(q) + ')'] = gcd(2,q-1)
                        # Note that type B and C are isomorphic if q=2**k, so we do not add duplicates
                        if n>2 and prime != 2:
                            self.current_group_multiplier_list['S' + str(2*n) + '(' + str(q) + ')'] = gcd(2,q-1)
                    elif compatible and not self.multipliers:
                        self.current_group_list.append('O' + str(2*n+1) + '(' + str(q) + ')')
                        if n>2 and prime != 2:
                            self.current_group_list.append('S' + str(2*n) + '(' + str(q) + ')')
                    n += 1


    def chevalley_D(self):
        # Notice: if q=2**k then gcd(4,q**n-1)=1 so first check condition still holds
        # Chevalley type D groups depend on n and q=prime**k, n>3
        # First compatibility check n*(n-1) = 12 (n=4)
        if max(self.order.values()) < 12:
            return
        # We determine compatible primes
        compatible_primes = []
        for prime in self.primes:
            if self.order[prime] >= 12:
                compatible_primes.append(prime)
        # For each compatible prime 
        for prime in compatible_primes:
            # q=p**k is compatible if self.order[prime] >= 12*k
            for k in range(1,self.order[prime]//12+1):
                q = prime**k
                n = 4
                # We build the product term by adding the first two terms
                product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
                first_term_order = dict(factor(q**2-1))
                second_term_order = dict(factor(q**4-1))
                # We check if the first terms' primes are compatible
                if set(first_term_order.keys()) <= self.primes:
                # We merge the first term order into product_order
                    for tprime in first_term_order:
                        product_order[tprime] += first_term_order[tprime]
                else:
                    # If they are not compatible we go next k
                    continue
                # We check if the second terms' primes are compatible
                if set(second_term_order.keys()) <= self.primes:
                    # We merge the second term order into product_order
                    for tprime in second_term_order:
                        product_order[tprime] += second_term_order[tprime]
                else:
                    # If they are not compatible we go next k
                    continue
                # We continue building the product term for bigger n's
                # Since the order contains q**(n*(n-1)) we have a stopping condition to test each n
                compatible = True
                while self.order[prime] >= k*n*(n-1):
                    # We have to consider the extra term q**n-1 and gcd(4,q**n-1)
                    # Since q**n-1 changes for each n and we do not want to modify product_order we will create
                    # a relative order that takes the previous terms into account
                    extra_term_order = dict(factor(q**n-1))
                    # Notice that if q == 2**k then gcd(4,q**n-1)=1, as such
                    if prime != 2:
                        if gcd(4, q**n-1) == 2:
                            extra_term_order[2] -= 1
                        else:
                            extra_term_order[2] -= 2
                        # If division by gcd removes the factor 2 we remove it from the dictionary
                        if extra_term_order[2] == 0:
                            del extra_term_order[2]
                    # We check the compatibility of the previous term and create the relative order
                    relative_order = copy(self.order)
                    if set(extra_term_order.keys()) <= self.primes:
                        # We remove the extra term order from relative order
                        for tprime in extra_term_order:
                            relative_order[tprime] -= extra_term_order[tprime]
                    else:
                        # If they are not compatible we stop
                        compatible = False
                        break
                    # We build the order of the current term
                    term_order = dict(factor(q**(2*(n-1))-1))
                    # We check if prime factors are compatible
                    if set(term_order.keys()) <= self.primes:
                        # We merge the term order into product_order
                        for tprime in term_order:
                            product_order[tprime] += term_order[tprime]
                    else:
                        # If they are not compatible we stop
                        compatible = False
                        break
                    # We check prime orders compatibility
                    for pprime in product_order:
                        if product_order[pprime] > relative_order[pprime]:
                            compatible = False
                            break
                    # If prime orders are compatible we add the group
                    if compatible and self.multipliers :
                        if n == 4 and q == 2:
                            self.current_group_multiplier_list['O' + str(2*n) + '+' + '(' + str(q) + ')'] = 4
                        else:
                            self.current_group_multiplier_list['O' + str(2*n) + '+' + '(' + str(q) + ')'] = gcd(4,q**n-1)
                    elif compatible and not self.multipliers:
                        self.current_group_list.append('O' + str(2*n) + '+' + '(' + str(q) + ')')
                    n += 1


    def classical_chevalley(self):
        self.chevalley_A()
        self.chevalley_B_C()
        self.chevalley_D()

    def exceptional_chevalley_E6(self):
        # Notice: if q=3**k then gcd(3,q-1)=1 so first check condition still holds
                # First compatibility check
        if max(self.order.values()) < 36:
            return
        # We determine compatible primes
        compatible_primes = []
        for prime in self.primes:
            if self.order[prime] >= 36:
                compatible_primes.append(prime)
        # For each compatible prime 
        for prime in compatible_primes:
            # For each prime consider q = prime**k
            for k in range(1,self.order[prime] // 36 + 1):
                # We build the order of the product term
                product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
                compatible = True
                for i in CHEVALLEY_E6_POWER_INDICES:
                    # We build the order of the current term
                    term_order = dict(factor(prime**(k*i)-1))
                    # We check if prime factors are compatible
                    if set(term_order.keys()) <= self.primes:
                        # We merge the term order into product_order
                        for tprime in term_order:
                            product_order[tprime] += term_order[tprime]
                    else:
                        # If they are not compatible we stop
                        compatible = False
                        break
                # We add 1/gcd(3,q-1)
                if gcd(3,prime**k-1) != 1:
                    product_order[3] -= 1 
                # If primes are compatible we check prime orders
                if compatible:
                    for pprime in product_order:
                        if product_order[pprime] > self.order[pprime]:
                            compatible = False
                            break
                # If prime orders are compatible we add the group
                if compatible and self.multipliers :
                    self.current_group_multiplier_list['E6(' + str(prime**k) +')'] = gcd(3,prime**k-1)
                elif compatible and not self.multipliers:
                    self.current_group_list.append('E6(' + str(prime**k) +')')


    def exceptional_chevalley_E7(self):
        # Notice: if q=2**k then gcd(2,q-1)=1 so first check condition still holds
        # First compatibility check
        if max(self.order.values()) < 63:
            return
        # We determine compatible primes
        compatible_primes = []
        for prime in self.primes:
            if self.order[prime] >= 63:
                compatible_primes.append(prime)
        # For each compatible prime 
        for prime in compatible_primes:
            # For each prime consider q = prime**k
            for k in range(1,self.order[prime] // 63 + 1):
                # We build the order of the product term
                product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
                compatible = True
                for i in CHEVALLEY_E7_POWER_INDICES:
                    # We build the order of the current term
                    term_order = dict(factor(prime**(k*i)-1))
                    # We check if prime factors are compatible
                    if set(term_order.keys()) <= self.primes:
                        # We merge the term order into product_order
                        for tprime in term_order:
                            product_order[tprime] += term_order[tprime]
                    else:
                        # If they are not compatible we stop
                        compatible = False
                        break
                # We add 1/gcd(2,q-1)
                if prime != 2:
                    product_order[2] -= 1 
                # If primes are compatible we check prime orders
                if compatible:
                    for pprime in product_order:
                        if product_order[pprime] > self.order[pprime]:
                            compatible = False
                            break
                # If prime orders are compatible we add the group
                if compatible and self.multipliers :
                    self.current_group_multiplier_list['E7(' + str(prime**k) +')'] = gcd(2,prime**k-1)
                elif compatible and not self.multipliers:
                    self.current_group_list.append('E7(' + str(prime**k) +')')


    def exceptional_chevalley_E8(self):
        # First compatibility check
        if max(self.order.values()) < 120:
            return
        # We determine compatible primes
        compatible_primes = []
        for prime in self.primes:
            if self.order[prime] >= 120:
                compatible_primes.append(prime)
        # For each compatible prime 
        for prime in compatible_primes:
            # For each prime consider q = prime**k
            for k in range(1,self.order[prime] // 120 + 1):
                # We build the order of the product term
                product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
                compatible = True
                for i in CHEVALLEY_E8_POWER_INDICES:
                    # We build the order of the current term
                    term_order = dict(factor(prime**(k*i)-1))
                    # We check if prime factors are compatible
                    if set(term_order.keys()) <= self.primes:
                        # We merge the term order into product_order
                        for tprime in term_order:
                            product_order[tprime] += term_order[tprime]
                    else:
                        # If they are not compatible we stop
                        compatible = False
                        break
                # If primes are compatible we check prime orders
                if compatible:
                    for pprime in product_order:
                        if product_order[pprime] > self.order[pprime]:
                            compatible = False
                            break
                # If prime orders are compatible we add the group
                if compatible and self.multipliers :
                    self.current_group_multiplier_list['E8(' + str(prime**k) +')'] = 1
                elif compatible and not self.multipliers:
                    self.current_group_list.append('E8(' + str(prime**k) +')')


    def exceptional_chevalley_F4(self):
        # First compatibility check
        if max(self.order.values()) < 24:
            return
        # We determine compatible primes
        compatible_primes = []
        for prime in self.primes:
            if self.order[prime] >= 24:
                compatible_primes.append(prime)
        # For each compatible prime 
        for prime in compatible_primes:
            # For each prime consider q = prime**k
            for k in range(1,self.order[prime] // 24 + 1):
                # We build the order of the product term
                product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
                compatible = True
                for i in CHEVALLEY_F4_POWER_INDICES:
                    # We build the order of the current term
                    term_order = dict(factor(prime**(k*i)-1))
                    # We check if prime factors are compatible
                    if set(term_order.keys()) <= self.primes:
                        # We merge the term order into product_order
                        for tprime in term_order:
                            product_order[tprime] += term_order[tprime]
                    else:
                        # If they are not compatible we stop
                        compatible = False
                        break
                # If primes are compatible we check prime orders
                if compatible:
                    for pprime in product_order:
                        if product_order[pprime] > self.order[pprime]:
                            compatible = False
                            break
                # If prime orders are compatible we add the group
                if compatible and self.multipliers :
                    if prime == 2 and k == 1:
                        self.current_group_multiplier_list['F4(' + str(2) +')'] = 2
                    else:
                        self.current_group_multiplier_list['F4(' + str(prime**k) +')'] = 1
                elif compatible and not self.multipliers:
                    self.current_group_list.append('F4(' + str(prime**k) +')')

    def exceptional_chevalley_G2(self):
        # Notice: G2(2) is not simple
        # First compatibility check
        if max(self.order.values()) < 6:
            return
        # We determine compatible primes
        compatible_primes = []
        for prime in self.primes:
            if self.order[prime] >= 6:
                compatible_primes.append(prime)
        # For each compatible prime 
        for prime in compatible_primes:
            # For each prime consider q = prime**k
            for k in range(1,self.order[prime] // 6 + 1):
                if prime == 2 and k == 1:
                    continue
                # We build the order of the product term
                product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
                compatible = True
                for i in CHEVALLEY_G2_POWER_INDICES:
                    # We build the order of the current term
                    term_order = dict(factor(prime**(k*i)-1))
                    # We check if prime factors are compatible
                    if set(term_order.keys()) <= self.primes:
                        # We merge the term order into product_order
                        for tprime in term_order:
                            product_order[tprime] += term_order[tprime]
                    else:
                        # If they are not compatible we stop
                        compatible = False
                        break
                # If primes are compatible we check prime orders
                if compatible:
                    for pprime in product_order:
                        if product_order[pprime] > self.order[pprime]:
                            compatible = False
                            break
                # If prime orders are compatible we add the group
                if compatible and self.multipliers :
                    if prime == 3 and k == 1:
                        self.current_group_multiplier_list['G2(' + str(3) +')'] = 3
                    elif prime == 2 and k == 2:
                        self.current_group_multiplier_list['G2(' + str(4) +')'] = 2
                    else:
                        self.current_group_multiplier_list['G2(' + str(prime**k) +')'] = 1
                elif compatible and not self.multipliers:
                    self.current_group_list.append('G2(' + str(prime**k) +')')

    def exceptional_chevalley(self):
        self.exceptional_chevalley_E6()
        self.exceptional_chevalley_E7()
        self.exceptional_chevalley_E8()
        self.exceptional_chevalley_F4()
        self.exceptional_chevalley_G2()

    def steinberg_2A(self):
        # Steinberg type 2A groups depend on n and q=prime**k, n>1
        # First compatibility check
        if max(self.order.values()) < 3:
            return
        # We determine compatible primes
        compatible_primes = []
        for prime in self.primes:
            if self.order[prime] >= 3:
                compatible_primes.append(prime)
        # For each compatible prime 
        for prime in compatible_primes:
            # q=p**k is compatible if self.order[prime] >= 3*k
            for k in range(1, self.order[prime] // 3 + 1):
                q = prime**k
                n = 2
                # We will build the order of the product term iteratibly for each q
                product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
                # We add the first term to the product term
                first_term_order = dict(factor(q**2-1))
                for ftprime in first_term_order:
                    if ftprime in product_order.keys():
                        product_order[ftprime] += first_term_order[ftprime]
                    else:
                        product_order[ftprime] = first_term_order[ftprime]
                # Since the order contains q**(n*(n+1)/2) we have a stopping condition to test each n
                compatible = True
                while self.order[prime] >= k*n*(n+1)/2:
                    # We build the term of the product for the current n
                    term_order = dict(factor(q**(n+1)-(-1)**(n+1)))
                    # We build product order now, notice it may have primes not found in it already
                    for tprime in term_order:
                        if tprime in self.primes:
                            product_order[tprime] += term_order[tprime]
                        else:
                            product_order[tprime] = term_order[tprime]
                    # We cannot modify product_order since we may need it in next iteration
                    # so we create a relative product order to take care of the gcd term
                    relative_product_order = copy(product_order)
                    # We add 1/(gcd(n+1,q+1)), notice it divides q**2-1
                    if gcd(n+1,q+1) != 1:
                        gcd_factors = dict(factor(gcd(n+1,q+1)))
                        # gcd_factors may cancel primes not contained in self.primes, so we remove such cases
                        for gprime in gcd_factors:
                            relative_product_order[gprime] -= gcd_factors[gprime]
                        for gprime in set(relative_product_order).difference(self.primes):
                            if relative_product_order[gprime] == 0:
                                del relative_product_order[gprime]
                        
                    # We check prime factors compatibility
                    if not set(relative_product_order.keys()) <= self.primes :
                        # If they are not compatible
                        compatible = False
                    
                    # We now check prime order compatibility against the relative order
                    if compatible:
                        for pprime in product_order:
                            if relative_product_order[pprime] > self.order[pprime]:
                                compatible = False
                                break
                    # If prime orders are compatible we add the group
                    # Notice: (q,n)=(2,2) is not simple
                    if compatible and (q == 2 and n == 2):
                        n += 1
                        continue
                    if compatible and self.multipliers:
                        if q == 2 and n == 3:
                            self.current_group_multiplier_list['U' + str(n+1) + '(' + str(q) + ')'] = 2
                        elif q == 3 and n == 3:
                            self.current_group_multiplier_list['U' + str(n+1) + '(' + str(q) + ')'] = 36
                        elif q == 2 and n == 5:
                            self.current_group_multiplier_list['U' + str(n+1) + '(' + str(q) + ')'] = 12
                        else:
                            self.current_group_multiplier_list['U' + str(n+1) + '(' + str(q) + ')'] = gcd(n+1,q+1)
                    elif compatible and not self.multipliers:
                        self.current_group_list.append('U' + str(n+1) + '(' + str(q) + ')')
                    # We increase n by 1
                    n += 1

    
    def steinberg_2D(self):
        # Notice: if q=2**k then gcd(4,q**n+1)=1 so first check condition still holds
        # Steinberg type 2D groups depend on n and q=prime**k, n>3
        # First compatibility check n*(n-1) = 12 (n=4)
        if max(self.order.values()) < 12:
            return
        # We determine compatible primes
        compatible_primes = []
        for prime in self.primes:
            if self.order[prime] >= 12:
                compatible_primes.append(prime)
        # For each compatible prime 
        for prime in compatible_primes:
            # q=p**k is compatible if self.order[prime] >= 12*k
            for k in range(1,self.order[prime]//12+1):
                q = prime**k
                n = 4
                # We build the product term by adding the first two terms
                product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
                first_term_order = dict(factor(q**2-1))
                second_term_order = dict(factor(q**4-1))
                # We check if the first terms' primes are compatible
                if set(first_term_order.keys()) <= self.primes:
                # We merge the first term order into product_order
                    for tprime in first_term_order:
                        product_order[tprime] += first_term_order[tprime]
                else:
                    # If they are not compatible we go next k
                    continue
                # We check if the second terms' primes are compatible
                if set(second_term_order.keys()) <= self.primes:
                    # We merge the second term order into product_order
                    for tprime in second_term_order:
                        product_order[tprime] += second_term_order[tprime]
                else:
                    # If they are not compatible we go next k
                    continue
                # We continue building the product term for bigger n's
                # Since the order contains q**(n*(n-1)) we have a stopping condition to test each n
                compatible = True
                while self.order[prime] >= k*n*(n-1):
                    # We have to consider the extra term q**n-1 and gcd(4,q**n+1)
                    # Since q**n-1 changes for each n and we do not want to modify product_order we will create
                    # a relative order that takes the previous terms into account
                    extra_term_order = dict(factor(q**n+1))
                    # Notice that if q == 2**k then gcd(4,q**n+1)=1, as such
                    if prime != 2:
                        if gcd(4, q**n+1) == 2:
                            extra_term_order[2] -= 1
                        else:
                            extra_term_order[2] -= 2
                        # If division by gcd removes the factor 2 we remove it from the dictionary
                        if extra_term_order[2] == 0:
                            del extra_term_order[2]
                    # We check the compatibility of the previous term and create the relative order
                    relative_order = copy(self.order)
                    if set(extra_term_order.keys()) <= self.primes:
                        # We remove the extra term order from relative order
                        for tprime in extra_term_order:
                            relative_order[tprime] -= extra_term_order[tprime]
                    else:
                        # If they are not compatible we stop
                        compatible = False
                        break
                    # We build the order of the current term
                    term_order = dict(factor(q**(2*(n-1))-1))
                    # We check if prime factors are compatible
                    if set(term_order.keys()) <= self.primes:
                        # We merge the term order into product_order
                        for tprime in term_order:
                            product_order[tprime] += term_order[tprime]
                    else:
                        # If they are not compatible we stop
                        compatible = False
                        break
                    # We check prime orders compatibility
                    for pprime in product_order:
                        if product_order[pprime] > relative_order[pprime]:
                            compatible = False
                            break
                    if compatible and self.multipliers :
                        if n == 4 and q == 2:
                            self.current_group_multiplier_list['O' + str(2*n) + '-' + '(' + str(q) + ')'] = 4
                        else:
                            self.current_group_multiplier_list['O' + str(2*n) + '-' + '(' + str(q) + ')'] = gcd(4,q**n+1)
                    elif compatible and not self.multipliers:
                        self.current_group_list.append('O' + str(2*n) + '-' + '(' + str(q) + ')')
                    n += 1


    def classical_steinberg(self):
        self.steinberg_2A()
        self.steinberg_2D()
    
    def exceptional_steinberg_2E6(self):
        # First compatibility check
        if max(self.order.values()) < 36:
            return
        # We determine compatible primes
        compatible_primes = []
        for prime in self.primes:
            if self.order[prime] >= 36:
                compatible_primes.append(prime)
        # For each compatible prime 
        for prime in compatible_primes:
            # For each prime consider q = prime**k
            for k in range(1,self.order[prime] // 36 + 1):
                # We build the order of the product term
                product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
                compatible = True
                for i in STEINBERG_2E6_POWER_INDICES:
                    # We build the order of the current term
                    term_order = dict(factor(prime**(k*i)-(-1)**i))
                    # We check if prime factors are compatible
                    if set(term_order.keys()) <= self.primes:
                        # We merge the term order into product_order
                        for tprime in term_order:
                            product_order[tprime] += term_order[tprime]
                    else:
                        # If they are not compatible we stop
                        compatible = False
                        break
                # We add 1/gcd(3,q+1)
                if gcd(3,prime**k+1) != 1:
                    product_order[3] -= 1
                # If primes are compatible we check prime orders
                if compatible:
                    for pprime in product_order:
                        if product_order[pprime] > self.order[pprime]:
                            compatible = False
                            break
                # If prime orders are compatible we add the group
                if compatible and self.multipliers :
                    if prime == 2 and k == 1:
                        self.current_group_multiplier_list['2E6(' + str(3) +')'] = 12
                    else:
                        self.current_group_multiplier_list['2E6(' + str(prime**k) +')'] = gcd(3,prime**k+1)
                elif compatible and not self.multipliers:
                    self.current_group_list.append('2E6(' + str(prime**k) +')')

    def exceptional_steinberg_3D4(self):
        # First compatibility check
        if max(self.order.values()) < 12:
            return
        # We determine compatible primes
        compatible_primes = []
        for prime in self.primes:
            if self.order[prime] >= 12:
                compatible_primes.append(prime)
        # For each compatible prime 
        for prime in compatible_primes:
            # For each prime consider q = prime**k
            for k in range(1,self.order[prime] // 12 + 1):
                # We build the order of the product term
                product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
                compatible = True
                q = prime**k
                for term in [q**8+q**4+1, q**6-1, q**2-1]:
                    # We build the order of the current term
                    term_order = dict(factor(term))
                    # We check if prime factors are compatible
                    if set(term_order.keys()) <= self.primes:
                        # We merge the term order into product_order
                        for tprime in term_order:
                            product_order[tprime] += term_order[tprime]
                    else:
                        # If they are not compatible we stop
                        compatible = False
                        break
                # If primes are compatible we check prime orders
                if compatible:
                    for pprime in product_order:
                        if product_order[pprime] > self.order[pprime]:
                            compatible = False
                            break
                # If prime orders are compatible we add the group
                if compatible and self.multipliers :
                    self.current_group_multiplier_list['3D4(' + str(q) +')'] = 1
                elif compatible and not self.multipliers:
                    self.current_group_list.append('3D4(' + str(q) +')')

    def exceptional_steinberg(self):
        self.exceptional_steinberg_2E6()
        self.exceptional_steinberg_3D4()

    def suzuki(self):
        # Suzuki groups all have powers of 2
        if 2 not in self.primes:
            return
        # First compatibility check
        if self.order[2] < 6:
            return
        # Since q=2**(2n+1) we have q**2 = q**(4n+2), we start at n=1
        n = 1
        while 4*n+2 <= self.order[2]:
            q = 2**(2*n+1)
            # We build the order of the product term
            product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
            compatible = True
            for term in [q**2+1, q-1]:
                # We build the order of the current term
                term_order = dict(factor(term))
                # We check if prime factors are compatible
                if set(term_order.keys()) <= self.primes:
                    # We merge the term order into product_order
                    for tprime in term_order:
                        product_order[tprime] += term_order[tprime]
                else:
                    # If they are not compatible we stop
                    compatible = False
                    break
            # If primes are compatible we check prime orders
            if compatible:
                for pprime in product_order:
                    if product_order[pprime] > self.order[pprime]:
                        compatible = False
                        break
            # If prime orders are compatible we add the group
            if compatible and self.multipliers :
                if n==1:
                    self.current_group_multiplier_list['Sz(' + str(8) +')'] = 4
                else:
                    self.current_group_multiplier_list['Sz(' + str(q) +')'] = 1
            elif compatible and not self.multipliers:
                self.current_group_list.append('Sz(' + str(q) +')')
            # Increase n
            n+=1

    def ree_tits(self):
        # Suzuki groups all have powers of 2
        if 2 not in self.primes:
            return
        # We check Tits group
        if set(TITS_ORDER.keys()) <= self.primes:
                compatible = True
                # We check if prime order is compatible
                for prime in TITS_ORDER:
                    if TITS_ORDER[prime] > self.order[prime]:
                        compatible = False
                        break
                if compatible and self.multipliers :
                    self.current_group_multiplier_list['2F4(2)\''] = 1
                elif compatible and not self.multipliers:
                    self.current_group_list.append('2F4(2)\'')
        # We check Ree 2F4 groups
        # First compatibility check
        if self.order[2] < 36:
            return
        # Since q=2**(2n+1) we have q**12 = q**(24n+12), we start at n=1
        n = 1
        while 24*n+12 <= self.order[2]:
            q = 2**(2*n+1)
            # We build the order of the product term
            product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
            compatible = True
            for term in [q**6+1, q**4-1, q**3+1, q-1]:
                # We build the order of the current term
                term_order = dict(factor(term))
                # We check if prime factors are compatible
                if set(term_order.keys()) <= self.primes:
                    # We merge the term order into product_order
                    for tprime in term_order:
                        product_order[tprime] += term_order[tprime]
                else:
                    # If they are not compatible we stop
                    compatible = False
                    break
            # If primes are compatible we check prime orders
            if compatible:
                for pprime in product_order:
                    if product_order[pprime] > self.order[pprime]:
                        compatible = False
                        break
            # If prime orders are compatible we add the group
            if compatible and self.multipliers :
                self.current_group_multiplier_list['2F4(' + str(q) + ')'] = 1
            elif compatible and not self.multipliers:
                self.current_group_list.append('2F4(' + str(q) +')')
            # Increase n
            n+=1

    
    def ree_2G2(self):
        # Ree 2G2 groups all have powers of 3
        if 3 not in self.primes:
            return
        # First compatibility check
        if self.order[3] < 9:
            return
        # Since q=3**(2n+1) we have q**3 = q**(6n+3), we start at n=1
        n = 1
        while 6*n+3 <= self.order[3]:
            q = 3**(2*n+1)
            # We build the order of the product term
            product_order = dict((list(self.primes)[j],0) for j in range(len(self.primes)))
            compatible = True
            for term in [q**3+1, q-1]:
                # We build the order of the current term
                term_order = dict(factor(term))
                # We check if prime factors are compatible
                if set(term_order.keys()) <= self.primes:
                    # We merge the term order into product_order
                    for tprime in term_order:
                        product_order[tprime] += term_order[tprime]
                else:
                    # If they are not compatible we stop
                    compatible = False
                    break
            # If primes are compatible we check prime orders
            if compatible:
                for pprime in product_order:
                    if product_order[pprime] > self.order[pprime]:
                        compatible = False
                        break
            # If prime orders are compatible we add the group
            if compatible and self.multipliers :
                self.current_group_multiplier_list['R(' + str(q) +')'] = 1
            elif compatible and not self.multipliers:
                self.current_group_list.append('R(' + str(q) +')')
            # Increase n
            n += 1

    def __clean_duplicates_full_check__(self):
        if self.multipliers:
            if 'A5' in self.current_group_multiplier_list :
                del self.current_group_multiplier_list['L2(4)']
                del self.current_group_multiplier_list['L2(5)']
            if 'A6' in self.current_group_multiplier_list :
                del self.current_group_multiplier_list['L2(9)']
            if 'A8' in self.current_group_multiplier_list :
                del self.current_group_multiplier_list['L4(2)']
            if 'L3(2)' in self.current_group_multiplier_list :
                del self.current_group_multiplier_list['L2(7)']
            if 'U4(2)' in self.current_group_multiplier_list :
                del self.current_group_multiplier_list['O5(3)']
        else:
            if 'A5' in self.current_group_list :
                self.current_group_list.remove('L2(4)')
                self.current_group_list.remove('L2(5)')
            if 'A6' in self.current_group_list :
                self.current_group_list.remove('L2(9)')
            if 'A8' in self.current_group_list :
                self.current_group_list.remove('L4(2)')
            if 'L3(2)' in self.current_group_list :
                self.current_group_list.remove('L2(7)')
            if 'U4(2)' in self.current_group_list :
                self.current_group_list.remove('O5(3)')

    def full_check(self):
        self.alternating()
        self.sporadic()
        self.classical_chevalley()
        self.exceptional_chevalley()
        self.classical_steinberg()
        self.exceptional_steinberg()
        self.suzuki()
        self.ree_2G2()
        self.ree_tits()
        self.__clean_duplicates_full_check__()

    def standard_notation(self):
        if self.multipliers:
            key_list = list(self.current_group_multiplier_list.keys())
            standardized_group_list = dict()
            for group in key_list:
                if group[0] in ['L', 'U', 'O'] and group not in SPORADIC_ORDERS:
                    standardized_group_list['PS' + group] = self.current_group_multiplier_list[group]
                elif group[0] == 'S' and group[1] != 'z' and group not in SPORADIC_ORDERS:
                    standardized_group_list['PSp' + group[1:]] = self.current_group_multiplier_list[group]
                else:
                    standardized_group_list[group] = self.current_group_multiplier_list[group]
            return standardized_group_list
        else:
            standardized_group_list = []
            for i in range(len(self.current_group_list)):
                if self.current_group_list[i][0] in ['L', 'U', 'O'] and self.current_group_list[i] not in SPORADIC_ORDERS:
                    standardized_group_list.append('PS' + self.current_group_list[i])
                elif self.current_group_list[i][0] == 'S' and self.current_group_list[i][1] != 'z' and self.current_group_list[i] not in SPORADIC_ORDERS:
                    standardized_group_list.append('PSp' + self.current_group_list[i][1:])
                else:
                    standardized_group_list.append(self.current_group_list[i])
            return standardized_group_list


# GROUP ORDER FUNCTIONS

CHEVALLEY_E6_POWER_INDICES = [2,5,6,8,9,12]
CHEVALLEY_E7_POWER_INDICES = [2,6,8,10,12,14,18]
CHEVALLEY_E8_POWER_INDICES = [2,8,12,14,18,20,24,30]
CHEVALLEY_F4_POWER_INDICES = [2,6,8,12]
CHEVALLEY_G2_POWER_INDICES = [2,6]
STEINBERG_2E6_POWER_INDICES = [2,5,6,8,9,12]

TITS_ORDER = {2: 11, 3: 3, 5: 2, 13: 1}

def alternating_order(n):
    return dict(factor(factorial(n)/2))

def exceptional_chevalley_E8_order(q):
    prime, power = factor(q)[0]
    order = {prime : power*120}
    for i in CHEVALLEY_E8_POWER_INDICES:
        term_order = dict(factor(q**i-1))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We reorder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order

def exceptional_chevalley_F4_order(q):
    prime, power = factor(q)[0]
    order = {prime : power*24}
    for i in CHEVALLEY_F4_POWER_INDICES:
        term_order = dict(factor(q**i-1))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We reorder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order

def exceptional_chevalley_G2_order(q):
    prime, power = factor(q)[0]
    order = {prime : power*6}
    for i in CHEVALLEY_G2_POWER_INDICES:
        term_order = dict(factor(q**i-1))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We reorder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order
    
def exceptional_chevalley_E6_order(q):
    prime, power = factor(q)[0]
    order = {prime : power*36}
    for i in CHEVALLEY_E6_POWER_INDICES:
        term_order = dict(factor(q**i-1))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We add 1/gcd(3,q-1)
    if gcd(3,q-1) != 1:
        order[3] -= 1
    # We reorder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order

def exceptional_chevalley_E7_order(q):
    prime, power = factor(q)[0]
    order = {prime : power*63}
    for i in CHEVALLEY_E7_POWER_INDICES:
        term_order = dict(factor(q**i-1))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We add 1/gcd(3,q-1)
    if gcd(2,q-1) != 1:
        order[2] -= 1
    # We reorder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order

def exceptional_steinberg_3D4_order(q):
    prime, power = factor(q)[0]
    order = {prime : power*12}
    for term in [q**8+q**4+1, q**6-1, q**2-1]:
        term_order = dict(factor(term))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We reorder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order   

def exceptional_steinberg_2E6_order(q):
    prime, power = factor(q)[0]
    order = {prime : power*36}
    for i in STEINBERG_2E6_POWER_INDICES:
        term_order = dict(factor(q**i-(-1)**(i)))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We add 1/gcd(3,q+1)
    if gcd(3,q+1) != 1:
        order[3] -= 1
    # We reorder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order

def suzuki_order(n):
    # Sz(q) where q = 2**(2*n+1)
    q = 2**(2*n+1)
    order = {2:4*n+2}
    for term in [q**2+1,q-1]:
        term_order = dict(factor(term))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We reorder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order

def ree_tits_order(n):
    # Tits group
    if n==0:
        return TITS_ORDER
    # 2F4(q) where q = 2**(2*n+1), n>0
    q = 2**(2*n+1)
    order = {2:24*n+12}
    for term in [q**6+1, q**4-1, q**3+1, q-1]:
        term_order = dict(factor(term))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We reorder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order

def ree_2G2_order(n):
    # 2G2(q) where q = 2**(2*n+1), n>0
    q = 3**(2*n+1)
    order = {3:6*n+3}
    for term in [q**3+1, q-1]:
        term_order = dict(factor(term))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We reorder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order

def chevalley_A_order(q,n):
    # q = p**k
    p, k = factor(q)[0]
    # We add first term
    order = {p:(1/2*n*(n+1)*k)}
    # We add product term
    for i in range(1,n+1):
        term_order = dict(factor(q**(i+1)-1))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We adjust gcd(n+1,q-1)
    if gcd(n+1,q-1) != 1:
        gcd_primes = dict(factor(gcd(n+1,q-1)))
        for prime in gcd_primes:
            order[prime] -= gcd_primes[prime]
    # We reoder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order

def chevalley_B_order(q,n):
    # q = p**k
    p, k = factor(q)[0]
    # We add first term
    order = {p:k*n**2}
    # We add product term
    for i in range(1,n+1):
        term_order = dict(factor(q**(2*i)-1))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We adjust gcd(2,q-1)
    if p != 2:
        order[2] -= 1
    # We reoder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order

def chevalley_C_order(q,n):
    # q = p**k
    p, k = factor(q)[0]
    # We add first term
    order = {p:k*n**2}
    # We add product term
    for i in range(1,n+1):
        term_order = dict(factor(q**(2*i)-1))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We adjust gcd(2,q-1)
    if p != 2:
        order[2] -= 1
    # We reoder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order

def steinberg_2A_order(q,n):
    # q = p**k
    p, k = factor(q)[0]
    # We add first term
    order = {p:(1/2*n*(n+1)*k)}
    # We add product term
    for i in range(1,n+1):
        term_order = dict(factor(q**(i+1)-(-1)**(i+1)))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We adjust gcd(n+1,q+1)
    if gcd(n+1,q+1) != 1:
        gcd_primes = dict(factor(gcd(n+1,q+1)))
        for prime in gcd_primes:
            order[prime] -= gcd_primes[prime]
    # We reoder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order

def chevalley_D_order(q,n):
    # q = p**k
    p, k = factor(q)[0]
    # We add first term
    order = {p:(n*(n-1)*k)}
    # We add product term
    for i in range(1,n):
        term_order = dict(factor(q**(2*i)-1))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We add the extra term q**n-1
    extra_term_order = dict(factor(q**n-1))
    for prime in set(extra_term_order.keys()).intersection(set(order.keys())):
        order[prime] += extra_term_order[prime]
    for new_prime in set(extra_term_order.keys()).difference(set(order.keys())):
        order[new_prime] = extra_term_order[new_prime]
    # We adjust gcd(4,q**n-1)
    if p != 2:
        order[2] -= factor(gcd(4,q**n-1))[0][1]
    # We reoder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order

def steinberg_2D_order(q,n):
    # q = p**k
    p, k = factor(q)[0]
    # We add first term
    order = {p:(n*(n-1)*k)}
    # We add product term
    for i in range(1,n):
        term_order = dict(factor(q**(2*i)-1))
        for prime in set(term_order.keys()).intersection(set(order.keys())):
            order[prime] += term_order[prime]
        for new_prime in set(term_order.keys()).difference(set(order.keys())):
            order[new_prime] = term_order[new_prime]
    # We add the extra term q**n+1
    extra_term_order = dict(factor(q**n+1))
    for prime in set(extra_term_order.keys()).intersection(set(order.keys())):
            order[prime] += extra_term_order[prime]
    for new_prime in set(extra_term_order.keys()).difference(set(order.keys())):
        order[new_prime] = extra_term_order[new_prime]
    # We adjust gcd(4,q**n+1)
    if p != 2:
        order[2] -= factor(gcd(4,q**n+1))[0][1]
    # We reoder the primes
    ordered_order = dict()
    for p in sorted(order):
        ordered_order[p] = order[p]
    return ordered_order
    

## BOUND BUILDER

def build_bound(n):
    # Primes using bound 2n+1
    primes = prime_range(2*n+2)
    order = dict([(p, 0) for p in primes])
    bounds6 = dict([(p, 0) for p in primes])
    # Primes greater than n+1 may only appear once
    big_primes = []
    for p in primes:
        if p > n+1:
            order[p] = 1
            big_primes.append(p)
    for p in big_primes: primes.remove(p)
    # We build compatible n! for calculations
    n_factorial = dict([(p, 0) for p in primes])
    n_factorial_factors = dict(factor(factorial(n)))
    for p in n_factorial_factors:
        n_factorial[p] = n_factorial_factors[p]
    # We build 6-bounds
    max6 = 6**(n-1)
    for p in primes:
        v = 1
        while p**v <= max6:
            v += 1
        bounds6[p] = (v-1) + n_factorial[p]
    # Build Blichfeld's coprime bounds
    blichfeld_bound = dict([(p, 0) for p in primes])
    for p in blichfeld_bound:
        blichfeld_bound[p] = n-1 + n_factorial[p]
    # Check all bounds against each other directly
    for p in primes:
        order[p] = min(blichfeld_bound[p], bounds6[p])
    # Previous step is only valid for primes coprime to n, or if n is prime
    if not is_prime(n):
        excluded_primes = [t[0] for t in factor(n)]
        for p in excluded_primes:
            order[p] = bounds6[p]
    
    return order




## REPORT FUNCTION

def report(simplegroups: SimpleGroupsOrder, filename: str):
    if simplegroups.multipliers:
        with open(filename,'a') as file:
            file.write('------- ' + filename + ' data' + ' -------\n\n')
            file.write('Bound order: \t\t' + str(simplegroups.order))
            file.write('\n\nGroup name \t\t Schur mult \t\t\t Group Order \n')
            group_names_list = simplegroups.standard_notation()
            for group in group_names_list:
                file.write(group + '\t\t\t\t\t')
                file.write(str(group_names_list[group]) + '\t\t\t\t\t')
                if group in SPORADIC_ORDERS:
                    file.write(str(SPORADIC_ORDERS[group]))
                elif group[0] == 'A':
                    file.write(str(alternating_order(int(group[1:]))))
                elif group[0:3] == 'PSL':
                    n_string = ''
                    for s in group[3:]:
                        if s == '(':
                            break
                        else:
                            n_string += s
                    q_string = group[4+len(n_string):-1]
                    n0 = int(n_string)-1
                    q0 = int(q_string)
                    file.write(str(chevalley_A_order(q0,n0)))
                elif group[0:3] == 'PSp':
                    n_string = ''
                    for s in group[3:]:
                        if s == '(':
                            break
                        else:
                            n_string += s
                    q_string = group[4+len(n_string):-1]
                    n0 = int(n_string)//2
                    q0 = int(q_string)
                    file.write(str(chevalley_C_order(q0,n0)))
                elif group[0:3] == 'PSO' and '+' in group:
                        n_string = ''
                        for s in group[3:]:
                            if s == '+':
                                break
                            else:
                                n_string += s
                        q_string = group[5+len(n_string):-1]
                        n0 = int(n_string)//2
                        q0 = int(q_string)
                        file.write(str(chevalley_D_order(q0,n0)))
                elif group[0:3] == 'PSO' and '-' in group:
                        n_string = ''
                        for s in group[3:]:
                            if s == '-':
                                break
                            else:
                                n_string += s
                        q_string = group[5+len(n_string):-1]
                        n0 = int(n_string)//2
                        q0 = int(q_string)
                        file.write(str(steinberg_2D_order(q0,n0)))
                elif group[0:3] == 'PSO':
                    n_string = ''
                    for s in group[3:]:
                        if s == '(':
                            break
                        else:
                            n_string += s
                    q_string = group[4+len(n_string):-1]
                    n0 = (int(n_string)-1)//2
                    q0 = int(q_string)
                    file.write(str(chevalley_B_order(q0,n0)))
                elif group[0:3] == 'PSU':
                        n_string = ''
                        for s in group[3:]:
                            if s == '(':
                                break
                            else:
                                n_string += s
                        q_string = group[4+len(n_string):-1]
                        n0 = int(n_string)-1
                        q0 = int(q_string)
                        file.write(str(steinberg_2A_order(q0,n0)))
                file.write('\n')
            file.write("\n\nGAP names list (Non-Trivial): ")
            file.write(str([group for group in simplegroups.get_calculated_groups() if simplegroups.get_calculated_groups()[group] != 1]).replace('\'', '\"'))
            file.write("\n\nGAP names list (Trivial): ")
            file.write(str([group for group in simplegroups.get_calculated_groups() if simplegroups.get_calculated_groups()[group] == 1]).replace('\'', '\"').replace("2F4(2)\"","2F4(2)\'").replace("Fi24\"","Fi24\'"))
            file.write("\n\nFull Standard names list: ")
            file.write(str(list(group_names_list.keys())).replace('\'', '\"'))
        return True
    else:
        # Not implemented
        pass


## STANDARD NOTATION

def standardize(current_group_list):
    standardized_group_list = []
    for i in range(len(current_group_list)):
        if current_group_list[i][0] in ['L', 'U'] and current_group_list[i] not in SPORADIC_ORDERS:
            standardized_group_list.append('PS' + current_group_list[i])
        elif current_group_list[i][0] == 'O' and current_group_list[i] not in SPORADIC_ORDERS:
            if '+' in current_group_list[i] or '-' in current_group_list[i]:
                standardized_group_list.append('P' + current_group_list[i])
        elif current_group_list[i][0] == 'S' and current_group_list[i][1] != 'z' and current_group_list[i] not in SPORADIC_ORDERS:
            standardized_group_list.append('PSp' + current_group_list[i][1:])
        else:
            standardized_group_list.append(current_group_list[i])
    return standardized_group_list


LATEX_SPORADICS = {'M11' : '$M_{11}$', 'M12' : '$M_{12}$', 'M22' : '$M_{22}$', 'M23' : '$M_{23}$', 'M24' : '$M_{24}$', 'J1' : '$J_1$', 
                   'J2' : '$J_2$', 'J3' : '$J_3$', 'J4' : '$J_4$', 'Co1' : '$Co_1$', 'Co2' : '$Co_2$', 'Co3' : '$Co_3$', 'Fi22' : '$Fi_{22}$',
                   'Fi23' : '$Fi_{23}$', 'Fi24\'' : '$Fi_{24}\'$', 'HS' : '$HS$', 'McL' : '$McL$', 'He' : '$He$', 'Ru' : '$Ru$', 'Suz': '$Suz$',
                   'ON' : '$ON$', 'HN' : '$HN$', 'Ly' : '$Ly$', 'Th' : '$Th$', 'B' : '$B$', 'M' : '$M$'}


def standardize_latex(current_group_list):
    standardized_group_list = []
    for i in range(len(current_group_list)):
        if current_group_list[i] in SPORADIC_ORDERS:
            standardized_group_list.append(LATEX_SPORADICS[current_group_list[i]])
        elif current_group_list[i][0] in ['L', 'U']:
            number_split = current_group_list[i][1:].split('(')
            standardized_group_list.append('$PS' + current_group_list[i][0] + '_{' + number_split[0] + '}(' + number_split[1] + '$')
        elif current_group_list[i][0] == 'O':
            if '+' in current_group_list[i]:
                number_split = current_group_list[i][1:].split('+')
                standardized_group_list.append('$P\\Omega_{' + number_split[0] + '}^+' + number_split[1] + '$')
            elif '-' in current_group_list[i]:
                number_split = current_group_list[i][1:].split('-')
                standardized_group_list.append('$P\\Omega_{' + number_split[0] + '}^-' + number_split[1] + '$')
            else:
                number_split = current_group_list[i][1:].split('(')
                standardized_group_list.append('$\\Omega_{' + number_split[0] + '}(' + number_split[1] + '$')
        elif current_group_list[i][:2] == 'Sz':
            standardized_group_list.append('$' + current_group_list[i] + '$')
        elif current_group_list[i][0] == 'S':
            number_split = current_group_list[i][1:].split('(')
            standardized_group_list.append('$PSp_{'  + number_split[0] + '}(' + number_split[1] + '$')
        elif current_group_list[i][0] == 'A':
            standardized_group_list.append('$A_{' + current_group_list[i][1:] + '}$')
        elif current_group_list[i][0] == 'G':
            standardized_group_list.append('$G_2' + current_group_list[i][2:] + '$')
        elif current_group_list[i][0] == 'E':
            standardized_group_list.append('$E_' + current_group_list[i][1:] + '$')
        elif current_group_list[i][:2] == '2E':
            standardized_group_list.append('${}^2E_6' + current_group_list[i][3:] + '$')
        elif current_group_list[i][:2] == '2F':
            standardized_group_list.append('${}^2F_4' + current_group_list[i][3:] + '$')
        elif current_group_list[i][:2] == '3D':
            standardized_group_list.append('${}^3D_4' + current_group_list[i][3:] + '$')
        elif current_group_list[i][0] == 'R':
            standardized_group_list.append('$' + current_group_list[i] + '$')
        else:
            standardized_group_list.append('\\verb|' + current_group_list[i] + '|')
        
    return standardized_group_list

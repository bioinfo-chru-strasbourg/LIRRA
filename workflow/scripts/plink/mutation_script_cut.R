
#Chance sharing correction
if (chance.sharing.correction == TRUE){
	e = 0.01
	p = (median.allele.frequency)^2 + (1-median.allele.frequency)^2
	phi = (length.of.chromosome/100)/markers.on.chromosome
	loci = log(e)/log(p)
	cs.correction = loci*phi
	}
if (chance.sharing.correction == FALSE){cs.correction = 0}

#Age estimation and confidence intervals
cc = confidence.coefficient
l.lengths = (1/100)*l.lengths 
r.lengths = (1/100)*r.lengths
n = length(l.lengths)

#Assuming an 'independent' genealogy
if (n < 10){i.cs.correction = 0}
if (n >= 10){i.cs.correction = cs.correction}

length.correction = (sum(l.lengths) + sum(r.lengths) - 2*(n-1)*i.cs.correction)/(2*n)

sum.lengths = sum(l.lengths) + sum(r.lengths) + 2*length.correction - 2*(n-1)*i.cs.correction
b.c = (2*n-1)/(2*n)
i.tau.hat <- (b.c*2*n)/sum.lengths
g_l <- qgamma(shape=2*n,scale=1/(2*n*b.c),((1-cc)/2))
g_u <- qgamma(shape=2*n,scale=1/(2*n*b.c),(cc+(1-cc)/2))		
i.l = g_l*i.tau.hat
i.u = g_u*i.tau.hat

#Assuming a 'correlated' genealogy
length.correction = (sum(l.lengths) + sum(r.lengths) - 2*(n-1)*cs.correction)/(2*n)

longest.l.lengths = match(sort(l.lengths,decreasing=TRUE)[1], l.lengths)
l.lengths[longest.l.lengths] <- l.lengths[longest.l.lengths] + length.correction + cs.correction
longest.r.lengths = match(sort(r.lengths,decreasing=TRUE)[1], r.lengths)
r.lengths[longest.r.lengths] <- r.lengths[longest.r.lengths] + length.correction + cs.correction

lengths = l.lengths + r.lengths
lengths = lengths - 2*cs.correction
rho.hat = (n*(mean(lengths))^2 - var(lengths)*(1+2*n))/(n*(mean(lengths))^2 + var(lengths)*(n-1))
n.star = n/(1+(n-1)*rho.hat)
	if (n.star > n) {n.star = n}
	if (n.star < -n) {n.star = -n}		
b.c = (2*n.star-1)/(2*n.star)
c.tau.hat = (b.c*2*n)/sum(lengths)
	if (rho.hat < -2/(n-1)){n.star = n/(1+(n-1)*abs(rho.hat))}
	if (-2/(n-1) <= rho.hat & rho.hat < -1/(n-1)){n.star = n}
g_l = qgamma(shape=2*n.star,scale=1/(2*n.star*b.c),(1-cc)/2)
g_u = qgamma(shape=2*n.star,scale=1/(2*n.star*b.c),cc+(1-cc)/2)
c.l = g_l*c.tau.hat
c.u = g_u*c.tau.hat

#Print results
print(paste("Assuming an 'independent' genealogy: age estimate =", round(i.tau.hat, digits=1) ,"generations, with confidence interval", paste("(",round(i.l, digits=1),",",round(i.u, digits=1),")",sep="")), quote=FALSE); print(paste("Assuming a 'correlated' genealogy: age estimate =", round(c.tau.hat, digits=1) ,"generations, with confidence interval", paste("(",round(c.l, digits=1),",",round(c.u, digits=1),")",sep="")), quote=FALSE)
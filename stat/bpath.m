T=1;N=500;dt=T/N;

dW=sqrt(dt)*randn(1,N);
W = cumsum(dW);
%plot([0:dt:T],[0 W],'r-')
plot([0:dt:T],[0 dW],'r-')
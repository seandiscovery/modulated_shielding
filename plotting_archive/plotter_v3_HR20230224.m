% Z position is at -50 mm from 109.5
% voxel # is 
% X,Y 201x201x201 bins, 0.1 mm resolution
% clear all

centerX=100;   % X center bin 
centerY=100;   % Y center bin 
centerZ=100;   % Z center bin 
scaleX=0.1;     % mm/bin
scaleY=0.1;     % mm/bin
scaleZ=0.1;     % mm/bin
zValue=50;
ROI=[61 140];   % 40 bins = 4 mm on each side of 100
% fileID='NEW_2023-0224/SMART_6channel_allBlocked_W_fine_201bins.csv'
fileID='NEW_2023-0224/SMART_6channel_topUnblocked_W_fine_201bins.csv'
Threshold=500;  % Cut-off dose threshold
unProcessedNormPt=[3.2 0];

% 'SMART_6channel_topOpen_Titanium_csv.csv'
% 'SMART_6channel_allBlocked_Titanium_csv.csv'
% 'SMART_6channel_topUnblocked_Water_csv.csv' 

% 
% READ-IN files, and crop as necessary 
A = readtable(fileID,'NumHeaderLines',9); %import CSV: x,y,z,dose 

fprintf('file imported \n')
fprintf('raw array based on last read-in of file')

B=table2array(A);           % convert to array
indexZ=find(B(:,3)==zValue); % pick 2-D dose plane step#1 (indices @ zValue
C=B(indexZ,:);               % pick 2-D dose plane step #2 (anything @ zValue)

indexY=find(C(:,2)<=ROI(2) & C(:,2)>=ROI(1)); % crop y-values
D=C(indexY,:);
indexX=find(D(:,1)<=ROI(2) & D(:,1)>=ROI(1)); % crop X-values
E=D(indexX,:);

E1=zeros(length(E),1); E2=zeros(length(E),1);
% convert everything into mm and then create origin and offset
for i=1:length(E)
    E1(i,1)=(E(i,1)-centerX)*scaleX;
end

for i=1:length(E)
    E2(i,1)=(E(i,2)-centerY)*scaleY;
end

% for i=1:length(E)
%     E3(i,1)=(E(i,3)-centerZ)*scaleZ;
% end
unNormDose=E(:,4);



tempX=unProcessedNormPt(1);
[val,idx]=min(abs(E1-tempX));
normPtAbs(1)=E1(idx,1);

tempY=unProcessedNormPt(2);
[val,idx]=min(abs(E2-tempY));
normPtAbs(2)=E2(idx,1);

%perhaps more robust version https://www.mathworks.com/matlabcentral/answers/375710-find-nearest-value-to-specific-number
% [~,~,idx]=unique(round(abs(E1-n)),'stable');
% minVal=E1(idx==1,1);
fprintf('norm value approximated to nearest bin approximated, please check \n');
normPtAbs

DoseRxPt=unNormDose(find(E1==normPtAbs(1) & E2==normPtAbs(2)))
% DoseRxPt=1;
% DoseRxPt=1.3906e-05;
Dose=unNormDose./DoseRxPt*100; % percentage Rx 
% Dose=Dose./DoseRxPt; % Rx in % units

% fprintf('number > Threshold \n');
% numOverThreshold= length(find(Dose>Threshold))
% % Dose(Dose>Threshold) = 0;

%% contourplotter
fprintf('Generating contour plot \n')

% x=E1;
% y=E2;
% v=Dose(:,1);
% 
% F=scatteredInterpolant(x,y,v);
% 
% xm = [min(x):max(diff(x)):max(x)];
% ym = [min(y):max(diff(y)):max(y)];
% 
% [Xm,Ym] = meshgrid(xm, ym);
% % Interpolate Z values
% Z = F(Xm,Ym);
% % create contour plot
% [Cfig,h] = contour(Xm,Ym,Z,70:10:130);
% clabel(Cfig,h,'FontSize',10,'Color','red')
% 
% fprintf('Contour plot done, overlaying schematics \n')
% hold on

[X,Y] = meshgrid(E1, E2);
Z = griddata(E1,E2,Dose,X,Y);

% [Cfig,h] = contour(X, Y, Z, 50:10:200);
% [Cfig,h] = contourf(X, Y, Z,1e-8:1e-7:6e-7);
[Cfig,h] = contourf(X, Y, Z, 80:20:200);
clabel(Cfig,h,'FontSize',10,'Color','red')

% overlaying circles for clarity
hold on

% tandem
xCenter = 0;
yCenter = 0;
radius =3; 
theta = 0 : 0.01 : 2*pi;
xCirc = radius * cos(theta) + xCenter;
yCirc = radius * sin(theta) + yCenter;
plot(xCirc, yCirc, 'b-', 'LineWidth', 3);

% source
radius = .6; % in mm
xCirc = radius * cos(theta) + xCenter;
yCirc = radius * sin(theta) + yCenter;
fill(xCirc,yCirc,'g')

% % shielding rods - 4 channel setup
% radius = 0.9; % in mm
% xCirc = radius * cos(theta) + 1.8;
% yCirc = radius * sin(theta) + 0;
% fill(xCirc,yCirc,'b')
% xCirc = radius * cos(theta) + 0;
% yCirc = radius * sin(theta) + -1.8;
% fill(xCirc,yCirc,'b')
% xCirc = radius * cos(theta) + 0;
% yCirc = radius * sin(theta) + 1.8;
% fill(xCirc,yCirc,'b')
% xCirc = radius * cos(theta) + -1.8;
% yCirc = radius * sin(theta) + 0;
% fill(xCirc,yCirc,'b')
% 

% shielding rods - 6 channel setup
radius = 0.8; % in mm
yCirc = radius * cos(theta) + 1.8;
xCirc = radius * sin(theta) ;
fill(xCirc,yCirc,'w')
yCirc = radius * cos(theta) -1.8;
xCirc = radius * sin(theta) ;
fill(xCirc,yCirc,'b')
yCirc = radius * cos(theta) + 0.9;
xCirc = radius * sin(theta) + 1.56;
fill(xCirc,yCirc,'b')
yCirc = radius * cos(theta) + 0.9;
xCirc = radius * sin(theta) - 1.56;
fill(xCirc,yCirc,'b')
yCirc = radius * cos(theta) - 0.9;
xCirc = radius * sin(theta) + 1.56;
fill(xCirc,yCirc,'b')
yCirc = radius * cos(theta) - 0.9;
xCirc = radius * sin(theta) - 1.56;
fill(xCirc,yCirc,'b')

plot(normPtAbs(1),normPtAbs(2),'^');

axis([-4 4 -4 4])
% axis([-4 4 0 1e-3])
axis square


% % 
% % axis([-7.5 7.5 -7.5 7.5])
% % axis square
% 
% % extra contour code I found online
% % % Make some sample grayscale image
% % I = abs(sin((1:500)'/100)*sin((1:500)/100));
% % % Convert the grayscale image to RGB
% % Irgb = cat(3,I,I,I);
% % % Plot the image and some contours in color
% % image(Irgb)
% % hold all
% % contour(I);
% %
% %
% % R = sqrt(X.^2 + Y.^2) + eps;
% % Z = sin(R)./R;
% % 
% % % surface in 3D
% % figure;
% % surf(Z,'EdgeColor','None')
% % 
% % % 2D map using view
% % figure;
% % surf(Z,'EdgeColor','None');
% % view(2)
% % 
% % [X,Y] = meshgrid(-8:.5:8);
% % R = sqrt(X.^2 + Y.^2) + eps;
% % Z = sin(R)./R;
% % figure;
% % subplot(1,3,1);
% % pcolor(X,Y,Z); 
% % subplot(1,3,2);
% % pcolor(X,Y,Z); shading flat;
% % subplot(1,3,3);
% % pcolor(X,Y,Z); shading interp;
% 

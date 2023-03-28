%
%  Esta función recibe una matriz 2xn donde la primera fila corresponde 
%  a confidence y la segunda fila al valor de IoU correspondiente de acuerdo 
%  al valor de confidence
%
%   CIoU = [Confidence Confidence Confidence Confidence Confidence ...
%             IoU         IoU         IoU       IoU         IoU    ...]
%
%
%  1. Ordenar la matriz de acuerdo al valor de confidence de forma descendiente
%  2. Clasificación del valor de IoU como TruePositive (TP), FalsePositive(FP),
%     FalseNegative(FN), dada la variable de entrada IoUthresh
%
%     La clasificación esta dada por:
%     TP = 1
%     FP = 0
%     FN = -1
%     
%     La variable minConf indica la menor calificación posible para considerar 
%     una detección como positiva (TP), de lo contrario, se califica como FP
%
%     3. Cálculo de Precision y Recall
%     4. Cálculo de AP a través de integración por el método del trapecio
%         I = (b-a)( (f(a) + f(b)) / 2 )
%         El renglón de recall corresponde con a, mientras que precision con f(a)

function AP = averagePrec(CIoU, IoUthresh, minConf)
  
  %Ordenar la matriz de 2xN
  [~,s] = sort(CIoU(1,:),'descend');
  Matrix = CIoU(:,s);
  
  %Clasificación de acuerdo a IoUthresh y minConf
  for i = 1 : size(Matrix,2)
    if Matrix(1,i) == 0
      Matrix(3,i) = -1;
    elseif Matrix(1,i) < minConf || Matrix(2, i) == 0
      Matrix(3,i) = 0;      
    elseif Matrix(2,i) > IoUthresh
      Matrix(3,i) = 1;
    else 
      Matrix(3,i) = 0;
    endif
  endfor
  
  %Cálculo de Precision
  tp = 0;
  fp = 0;
  tpfn = 0;
  
  %Ciclo para encontrar la cantidad de tp y fn clasificados (denominador de recall)
  for i = 1 : size(Matrix,2)
    if Matrix(3,i) == 1 || Matrix(3,i) == -1
      tpfn = tpfn + 1;
    endif
  endfor
  
  %Ciclo para calculo de precision y recall
  for i = 1 : size(Matrix,2)
    if Matrix(3,i) == 1
      tp = tp + 1;
    elseif Matrix(3,i) == 0
      fp = fp + 1;
    endif
    
    if Matrix(3,i) != -1
      if tp != 0
        Matrix(4,i) = tp / (tp+fp);   %Renglón de Precision
        Matrix(5,i) = tp / tpfn;      %Renglón de Recall
      else
        Matrix(4,i) = 0;   %Renglón de Precision
        Matrix(5,i) = 0;   %Renglón de Recall
      endif
    else
      Matrix(4,i) = 0;   %Renglón de Precision
      Matrix(5,i) = 0;   %Renglón de Recall
    endif
    
  endfor
  
  %Results
  Matrix
  
  %Precision and Recall
  if tp != 0
    Precision = tp / (tp+fp)
    Recall = tp / tpfn
  else
    Precision = 0
    Recall = 0
  endif
  
  %Graficar solo los puntos diferentes de 0
  x=0;
  y=0;
  for i = 1 : size(Matrix,2)
    if Matrix(5,i) != 0
      x(1,i) = Matrix(5,i);
      y(1,i) = Matrix(4,i);
    endif
  endfor
  
  plot(x,y);
  
  %Intergación por el método del trapecio  I = (b-a)( (f(a) + f(b)) / 2 )
  i = 1;
  AP = 0;
  
  %La primera vez
  AP = (Matrix(5,1) - 0)*(1 + Matrix(4,1))/2;
  
  %disp('Entra al ciclo while');
  
  while Matrix(3,i) != -1 && i < tp
    AP = AP + ((Matrix(5,i+1) - Matrix(5,i))*(Matrix(4,i) + Matrix(4,i+1))/2);
    i = i+1;
  endwhile
    
endfunction

BEGIN{OFS= "\t"}
{  if (substr($0,131,4) >= minMagnitude) 
   { 

     # If depth is not provided, use default value of 7.5 km (average in CA)
     depth_str = substr($0, 44, 8); 
     print depth_str;
     if (depth_str ~ /^[ \t]+$/)
     {
       depth_str = 7.5
     }

     # If depth error is not provided, use default value of 5
     depth_error_str = substr($0, 95, 7); 
     print depth_error_str;
     if (depth_error_str ~ /^[ \t]+$/)
     {
       depth_error_str = 5
     }
        
     # Apply modulus(10) since depth error should not exceed 10km   
     depth = sprintf("%8.4f", depth_str);
     depth_error = sprintf("%7.4f", depth_error_str % 10);
     
     print substr($0,34,10),
           substr($0,25,9),
           substr($0,6,4),
           substr($0,10,2),
           substr($0,12,2),
           substr($0,130,5),
           depth, 
           substr($0,14,2),
           substr($0,16,2),
           substr($0,18,7),
           substr($0,88,7),
           depth_error,
           substr($0,54,3)}
}


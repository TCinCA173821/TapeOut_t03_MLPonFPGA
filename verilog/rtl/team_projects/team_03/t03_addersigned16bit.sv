module addersigned16bit(
    input logic signed [15:0] in1,
    input logic signed [15:0] in2,
    output logic signed [15:0] out
); 
    assign out = in1 + in2;
endmodule

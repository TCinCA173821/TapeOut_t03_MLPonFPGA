module mixedsign4bitmult(
    input logic signed [3:0] signedin1,
    input logic [3:0] unsignedin2,
    output logic signed [15:0] signextendedout
);
    assign signextendedout = $signed(signedin1) * $signed({1'b0,unsignedin2});
endmodule

module addersigned16bit(
    input logic signed [15:0] in1,
    input logic signed [15:0] in2,
    output logic signed [15:0] out
); 
    assign out = in1 + in2;
endmodule

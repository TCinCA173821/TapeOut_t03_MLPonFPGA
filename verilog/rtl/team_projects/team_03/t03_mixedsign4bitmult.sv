module mixedsign4bitmult(
    input logic signed [3:0] signedin1,
    input logic [3:0] unsignedin2,
    output logic signed [15:0] signextendedout
);
    assign signextendedout = $signed(signedin1) * $signed({1'b0,unsignedin2});
endmodule


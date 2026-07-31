module MAC( 
    input logic clk,
    input logic n_rst,
    input logic [7:0] MAC_in,
    input logic MAC_s,
    input logic MAC_l,
	output logic signed [15:0] MAC_out,
    output logic [3:0] MAC_outrelu
);
    logic signed [15:0] mult_out, reg_in;
    
    mixedsign4bitmult mult1 (.signedin1($signed(MAC_in[7:4])),.unsignedin2(MAC_in[3:0]),.signextendedout(mult_out));
    addersigned16bit adder1 (.in1(mult_out),.in2(MAC_out),.out(reg_in));
    accreg buf_reg1 (.clk(clk),.n_rst(n_rst),.wen(MAC_s),.len(MAC_l),.in(reg_in),.Lin(MAC_in),.out(MAC_out));
    relu relu1 (.in(MAC_out),.out(MAC_outrelu));
endmodule

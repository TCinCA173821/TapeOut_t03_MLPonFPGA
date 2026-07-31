module accreg(
    input logic clk,
    input logic n_rst,
    input logic wen,
    input logic len,
    input logic signed [15:0] in,
    input logic [7:0] Lin,
    output logic signed [15:0] out
);

    logic signed [15:0] reg_val, reg_val_nxt;
    always_ff @ (posedge clk, negedge n_rst) begin
        if(!n_rst) reg_val <= 16'd0;
        else reg_val <= reg_val_nxt;
    end

    always_comb begin
        if (len) reg_val_nxt = { {8{Lin[7]}}, Lin};
        else if(wen) reg_val_nxt = in;
        else reg_val_nxt = reg_val;
    end
    assign out = reg_val;
endmodule

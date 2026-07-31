module relu(
    input logic signed [15:0] in,
    output logic [3:0] out
); 
    always_comb begin
        if(in[15] == 1'b1) out = 4'd0;
        else if(|in[14:4]) out = 4'b1111;
        else out = in[3:0];
    end
endmodule

module dualffsync (
    input logic clk,
    input logic n_rst,
    input logic async_in,
    output logic sync_out
);
    logic syn1, syn2;
    always_ff @ (posedge clk, negedge n_rst) begin
        if(!n_rst) begin
            syn1 <= 1'b0;
            syn2 <= 1'b0;
        end else begin
            syn1 <= async_in;
            syn2 <= syn1;
        end
    end
    assign sync_out = syn2;
endmodule

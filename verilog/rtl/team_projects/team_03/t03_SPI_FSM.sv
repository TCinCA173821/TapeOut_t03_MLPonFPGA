module SPI_FSM(
    input logic clk,
    input logic n_rst,
    input logic sync_cs,
    input logic nxtpckt,
    output logic nxtpckt_to_pi,
    output logic SPI_dv
);
    typedef enum logic [1:0] { 
        IDLE,
        RQ,
        RECEIVE,
        PULSEDV
    } state_t;

    state_t curstate, nxtstate;

    always_ff @(posedge clk, negedge n_rst) begin
        if(!n_rst) curstate <= IDLE;
        else curstate <= nxtstate;
    end

    always_comb begin
        case(curstate)
            IDLE: nxtstate = nxtpckt ? RQ : IDLE;
            RQ: nxtstate = sync_cs ? RECEIVE : RQ;
            RECEIVE: nxtstate = sync_cs ? RECEIVE : PULSEDV;
            PULSEDV: nxtstate = IDLE;
        endcase
    end

    always_comb begin
        nxtpckt_to_pi = 1'b0;
        SPI_dv = 1'b0;
        case(curstate)
            RQ: nxtpckt_to_pi = 1'b1;
            PULSEDV: SPI_dv = 1'b1;
            default: begin
                nxtpckt_to_pi = 1'b0;
                SPI_dv = 1'b0;
            end
        endcase
    end
endmodule

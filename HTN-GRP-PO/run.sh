# python main.py --agent_type fixed_always_ask --max_depth 17 --num_sims 5 --d 0.95 --e 1 --wp -5 --qr 5 --qp -5 --domain kitchen 
# python main.py --agent_type pomdp --max_depth 19 --num_sims 6 --d 0.95 --e 1 --wp -5 --qr 5 --qp -5 --domain block
# python main.py --agent_type pomdp --max_depth 19 --num_sims 6 --d 0.95 --e 1 --wp -5 --qr 5 --qp -5 --domain block --dt 0.01
# python main.py --agent_type fixed_always_ask --max_depth 17 --num_sims 5 --d 0.95 --e 1 --wp -5 --qr 5 --qp -5 --domain block
# python main.py --agent_type htn --max_depth 17 --num_sims 5 --d 0.95 --e 1 --wp -5 --qr 5 --qp -5 --domain block
# python main.py --agent_type fixed_always_ask --max_depth 17 --num_sims 5 --d 0.95 --e 1 --wp -5 --qr 5 --qp -5 --domain block

# python main.py --agent_type pomdp --max_depth 19 --num_sims 6 --d 0.95 --e 1 --wp -5 --qr 5 --qp -5 --domain block --dt 0.01


python main.py --agent_type htn --max_depth 17 --num_sims 6 --d 0.95 --e 1.0 --wp -5 --qr 5 --qp -5 --domain kitchen 
python main.py --agent_type fixed_always_ask --max_depth 17 --num_sims 6 --d 0.95 --e 1.0 --wp -5 --qr 5 --qp -5 --domain kitchen 

/* ---------------------------------------------------------------------------


  This file is part of the ``ltl'' package of NuSMV version 2.
  Copyright (C) 1998-2001 by CMU and FBK-irst.

  NuSMV version 2 is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2 of the License, or (at your option) any later version.

  NuSMV version 2 is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this library; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.

  For more information on NuSMV see <http://nusmv.fbk.eu>
  or email to <nusmv-users@fbk.eu>.
  Please report bugs to <nusmv-users@fbk.eu>.

  To contact the NuSMV development board, email to <nusmv@fbk.eu>.

-----------------------------------------------------------------------------*/

/*!
  \author Marco Roveri
  \brief Shell commands to deal with the LTL model checking.

  Shell commands to deal with the LTL model checking.

*/


#if HAVE_CONFIG_H
# include "nusmv-config.h"
#endif

#include "nusmv/shell/cmd/cmd.h"
#include "nusmv/shell/ltl/ltlCmd.h"

#include "nusmv/core/utils/StreamMgr.h"
#include "nusmv/core/utils/ErrorMgr.h"
#include "nusmv/core/utils/error.h" /* for CATCH(errmgr) */

#include "nusmv/core/prop/Prop.h"
#include "nusmv/core/prop/propPkg.h"
#include "nusmv/core/prop/PropDb.h"

#include "nusmv/core/mc/mc.h"
#include "nusmv/core/enc/enc.h"
#include "nusmv/core/compile/compile.h" /* to check for presence of compassion */


// For pre image computation
#include "nusmv/core/fsm/bdd/BddFsm.h"
#include "nusmv/core/fsm/bdd/bdd.h"
#include "nusmv/core/fsm/bdd/bddInt.h"
#include "nusmv/core/fsm/bdd/BddFsm_private.h"

#include "nusmv/core/enc/operators.h"

//For computing execution time

#include <time.h>

/*---------------------------------------------------------------------------*/
/* Variable declarations                                                     */
/*---------------------------------------------------------------------------*/
extern cmp_struct_ptr cmps;

extern BddVarSet_ptr controllable;
extern BddVarSet_ptr notcontrollable;
extern BddVarSet_ptr pnfvars;



int CommandCheckLtlSpec(NuSMVEnv_ptr env, int argc, char** argv);

int CommandCheckRealizability(NuSMVEnv_ptr env, int argc, char** argv);

/*---------------------------------------------------------------------------*/
/* Static function prototypes                                                */
/*---------------------------------------------------------------------------*/
static int UsageCheckLtlSpec(const NuSMVEnv_ptr env);

/*---------------------------------------------------------------------------*/
/* Definition of exported functions                                          */
/*---------------------------------------------------------------------------*/

void Ltl_Init(NuSMVEnv_ptr env)
{
  Cmd_CommandAdd(env, "check_ltlspec", CommandCheckLtlSpec, 0, false); 
  Cmd_CommandAdd(env, "check_realizability", CommandCheckRealizability, 0, false);
}

boolean Realizable(NuSMVEnv_ptr env, BddFsm_ptr fsm, bdd_ptr property)
{
  bdd_ptr initial = Nil,  check_condition = Nil, old_bf = Nil, bf = Nil, notbf = Nil, tmp = Nil;
 
  int step = 0;
  boolean realizable = false;

  initial = BddFsm_get_init(fsm);

  //printf("initial\n");
  //dd_printminterm(fsm->dd, initial);
  
  

  bf = bdd_dup(property);

  old_bf = bdd_false(fsm->dd);

  while (old_bf != bf && !realizable)
  {
    printf("Step %d\n", step);
    step++;

    bdd_free(fsm->dd, old_bf);
    old_bf = bf;
    

    
   // bf = BddFsm_get_strong_pre_image_fa_ncontr_ex_contr_ex_pnf(fsm, old_bf); // strong preimage
    bf = BddFsm_get_strong_pre_image_ex_contr_fa_ncontr_ex_pnf(fsm, old_bf);
    
    //printf("bf\n");
    //dd_printminterm(fsm->dd, bf);

    bdd_or_accumulate(fsm->dd, &bf, old_bf);

    //printf("bf\n");
    //dd_printminterm(fsm->dd, bf);


    notbf = bdd_not(fsm->dd, bf);

    //printf("NOTbf\n");
    //dd_printminterm(fsm->dd, notbf);

    check_condition = bdd_and(fsm->dd, notbf, initial);

    

    //printf("check cond\n");
    //dd_printminterm(fsm->dd, check_condition);


    if (bdd_is_false(fsm->dd, check_condition))
    {
      realizable = true;
    }

    bdd_free(fsm->dd, notbf);
    bdd_free(fsm->dd, check_condition);
  }

  bdd_free(fsm->dd, old_bf);
  bdd_free(fsm->dd, bf);
  bdd_free(fsm->dd, initial);

  return realizable;
}

int CommandCheckRealizability(NuSMVEnv_ptr env, int argc, char** argv){

  BddFsm_ptr fsm = BDD_FSM(NuSMVEnv_get_value(env, ENV_BDD_FSM));
  node_ptr toplevel = (node_ptr)NuSMVEnv_get_value(env, ENV_REALIZABLE);
  bdd_ptr property;
  time_t start, end;
  
  
  
  double diff_time;

  property = BddEnc_expr_to_bdd(fsm->enc, toplevel, Nil);
  
  //dd_printminterm(fsm->dd, property);
  

  
  time(&start);
  if (Realizable(env, fsm, property)){
    printf("realizable\n");
  }
  else{
    printf("unrealizable\n");
  }
  time(&end);

  diff_time = difftime(end, start);

  printf("Execution time %f\n", diff_time);

  return 0;
}




/*!
  \command{check_ltlspec} Performs LTL model checking

  \command_args{[-h] [-m | -o output-file] [-n number | -p "ltl-expr [IN context]" | -P \"name\"] }

   Performs model checking of LTL formulas. LTL
  model checking is reduced to CTL model checking as described in the
  paper by [CGH97].<p>

  A <tt>ltl-expr</tt> to be checked can be specified at command line
  using option <tt>-p</tt>. Alternatively, option <tt>-n</tt> can be used
  for checking a particular formula in the property database. If
  neither <tt>-n</tt> nor <tt>-p</tt> are used, all the LTLSPEC formulas in
  the database are checked.<p>

  Command options:<p>
  <dl>
    <dt> <tt>-m</tt>
       <dd> Pipes the output generated by the command in processing
           <tt>LTLSPEC</tt>s to the program specified by the
           <tt>PAGER</tt> shell variable if defined, else
           through the Unix command "more".
    <dt> <tt>-o output-file</tt>
       <dd> Writes the output generated by the command in processing
           <tt>LTLSPEC</tt>s to the file <tt>output-file</tt>.
    <dt> <tt>-p "ltl-expr [IN context]"</tt>
       <dd> An LTL formula to be checked. <tt>context</tt> is the module
       instance name which the variables in <tt>ltl_expr</tt> must be
       evaluated in.
    <dt> <tt>-n number</tt>
       <dd> Checks the LTL property with index <tt>number</tt> in the property
            database.
    <dt> <tt>-P name</tt>
       <dd> Checks the LTL property named <tt>name</tt> in the property
            database.
  </dl>

*/

int CommandCheckLtlSpec(NuSMVEnv_ptr env, int argc, char** argv) // simile a un main
{
  const StreamMgr_ptr streams =
    STREAM_MGR(NuSMVEnv_get_value(env, ENV_STREAM_MANAGER));
  const ErrorMgr_ptr errmgr =
    ERROR_MGR(NuSMVEnv_get_value(env, ENV_ERROR_MANAGER));
  int c;
  int prop_no = -1;
  char* formula = NIL(char);
  char* formula_name = NIL(char);
  int status = 0;
  int useMore = 0;
  char* dbgFileName = NIL(char);
  FILE* outstream = StreamMgr_get_output_stream(streams);
  FILE* old_outstream = outstream;
  SymbTable_ptr st = SYMB_TABLE(NuSMVEnv_get_value(env, ENV_SYMB_TABLE));
  PropDb_ptr prop_db = PROP_DB(NuSMVEnv_get_value(env, ENV_PROP_DB));
  OptsHandler_ptr opts = OPTS_HANDLER(NuSMVEnv_get_value(env, ENV_OPTS_HANDLER));

  util_getopt_reset();
  while ((c = util_getopt(argc,argv,"hmo:n:p:P:")) != EOF) {

    switch (c) {
    case 'h': return UsageCheckLtlSpec(env);

    case 'n':
      if (formula != NIL(char)) return UsageCheckLtlSpec(env);
      if (prop_no != -1) return UsageCheckLtlSpec(env);
      if (formula_name != NIL(char)) return UsageCheckLtlSpec(env);

      prop_no = PropDb_get_prop_index_from_string(prop_db,
                                                  util_optarg);
      if (prop_no == -1) return 1;
      break;

    case 'P':
        if (formula != NIL(char)) return UsageCheckLtlSpec(env);
        if (prop_no != -1) return UsageCheckLtlSpec(env);
        if (formula_name != NIL(char)) return UsageCheckLtlSpec(env);

        formula_name = util_strsav(util_optarg);
        prop_no = PropDb_prop_parse_name(prop_db,
                                         formula_name);

        if (prop_no == -1) {
          StreamMgr_print_error(streams,  "No property named \"%s\"\n", formula_name);
          FREE(formula_name);
          return 1;
        }
        FREE(formula_name);
        break;

    case 'p':
      if (prop_no != -1) return UsageCheckLtlSpec(env);
      if (formula != NIL(char)) return UsageCheckLtlSpec(env);
      if (formula_name != NIL(char)) return UsageCheckLtlSpec(env);

      formula = util_strsav(util_optarg);
      break;

    case 'o':
      if (useMore == 1) return UsageCheckLtlSpec(env);
      dbgFileName = util_strsav(util_optarg);
      StreamMgr_print_output(streams,  "Output to file: %s\n", dbgFileName);
      break;

    case 'm':
      if (dbgFileName != NIL(char)) return UsageCheckLtlSpec(env);
      useMore = 1;
      break;

    default:  return UsageCheckLtlSpec(env);
    }
  }
  if (argc != util_optind) return UsageCheckLtlSpec(env);

  if (cmp_struct_get_read_model(cmps) == 0) {
    StreamMgr_print_error(streams,
            "A model must be read before. Use the \"read_model\" command.\n");
    return 1;
  }

  if (cmp_struct_get_encode_variables(cmps) == 0) {
    StreamMgr_print_error(streams,
            "The variables must be built before. Use the \"encode_variables\" command.\n");
    return 1;
  }

  if ( (!cmp_struct_get_build_model(cmps))
       && (opt_cone_of_influence(opts) == false) ) {
    StreamMgr_print_error(streams,  "The current partition method %s has not yet be computed.\n",
            TransType_to_string(get_partition_method(opts)));
    StreamMgr_print_error(streams,  "Use \t \"build_model -f -m %s\"\nto build the transition relation.\n",
            TransType_to_string(get_partition_method(opts)));
    return 1;
  }

  if (useMore || (char*)NULL != dbgFileName) {
    if (OUTCOME_SUCCESS !=
        Cmd_Misc_open_pipe_or_file(env, dbgFileName, &outstream)) {
      status = 1; goto check_ltlspec_exit;
    }
  }

  if (formula != NIL(char)) {
    prop_no = PropDb_prop_parse_and_add(prop_db, st,
                                        formula, Prop_Ltl, Nil);

    if (prop_no == -1) { status = 1; goto check_ltlspec_exit; }

    CATCH(errmgr) {
      PropDb_verify_prop_at_index(prop_db, prop_no);
    }
    FAIL(errmgr) {
      status = 1;
    }
  }
  else if (prop_no != -1) {
    if (Prop_check_type(PropDb_get_prop_at_index(
                  prop_db, prop_no), Prop_Ltl) != 0) {
      status = 1;
    }
    else {
      CATCH(errmgr) {
        PropDb_verify_prop_at_index(prop_db, prop_no);
      }
      FAIL(errmgr) {
        status = 1;
      }
    }
  }
  else {
    CATCH(errmgr) {
      PropDb_verify_all_type_wrapper(prop_db, Prop_Ltl);
    }
    FAIL(errmgr) {
      status = 1;
    }
  }

check_ltlspec_exit:
  if (useMore) {
    FILE* reset_stream;

    CmdClosePipe(outstream);
    reset_stream = StreamMgr_reset_output_stream(streams);
    StreamMgr_set_output_stream(streams, old_outstream);

    nusmv_assert(reset_stream == outstream);

    outstream = (FILE*)NULL;
  }

  if ((char*)NULL != dbgFileName) {
    /* this closes the file stream as well  */
    StreamMgr_set_output_stream(streams, old_outstream);

    outstream = (FILE*)NULL;
  }

  return status;
}

/*!
  \brief \todo Missing synopsis

  \todo Missing description
*/
static int UsageCheckLtlSpec(const NuSMVEnv_ptr env)
{
  StreamMgr_ptr streams = STREAM_MGR(NuSMVEnv_get_value(env, ENV_STREAM_MANAGER));
  StreamMgr_print_error(streams,  "usage: check_ltlspec [-h] [-m | -o file] [-n number | -p \"ltl_expr\" | -P \"name\"]\n");
  StreamMgr_print_error(streams,  "   -h \t\t\tPrints the command usage.\n");
  StreamMgr_print_error(streams,  "   -m \t\t\tPipes output through the program specified by\n");
  StreamMgr_print_error(streams,  "      \t\t\tthe \"PAGER\" environment variable if any,\n");
  StreamMgr_print_error(streams,  "      \t\t\telse through the UNIX command \"more\".\n");
  StreamMgr_print_error(streams,  "   -o file\t\tWrites the debugger output to \"file\".\n");
  StreamMgr_print_error(streams,  "   -n number\t\tChecks only the LTLSPEC with the given index number.\n");
  StreamMgr_print_error(streams,  "   -p \"ltl-expr\"\tChecks only the given LTL formula.\n");
  StreamMgr_print_error(streams,  "   -P \"name\"\t\tChecks only the LTLSPEC with the given name.\n");
  return(1);
}

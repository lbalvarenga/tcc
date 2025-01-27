qui {
	
cls
clear all
	
local BASE_PATH "\\wsl.localhost\Debian\home\lal\work\uel\tcc"
local BLOCK_PROMPT 1
  
cd `BASE_PATH'
do "utils\utils.do"
	
sysuse auto
import delimited "data\combinado.csv", clear

// Vars coletadas
label var date "Mês"
label var pibinfl "PIB Inflacionado (IGP-DI)"
label var igpdi "IGP-DI"
label var icbr "Commodities Brasil"
label var consap "Consumo Aparente"
label var pib "PIB"
label var cambio "Taxa de Câmbio (PTAX)"
label var ipca "IPCA"
label var selic "Taxa SELIC"

// Vars para gerar...
gen ivals = _n
gen months = tm(2002m1) + _n - 1
n tsset months, monthly


n _print "------- Geração das variáveis ln-------" 
gen ln_pibinfl = ln(pibinfl)
gen ln_igpdi = ln(igpdi)
gen ln_icbr = ln(icbr)
gen ln_consap = ln(consap)
gen ln_cambio = ln(cambio)
gen ln_ipca = ln(ipca)
gen ln_selic = ln(selic)

// TODO: ADF para todas vars

// Testes de estacionariedade
n _print "------- TESTES: DF-GLS, PP -------" 

n _print "*************** IPCA ****************"
n dfgls ln_ipca, maxlag(6)
n pperron ln_ipca

n _print "*************** Taxa de Câmbio (PTAX) ****************"
n dfgls ln_cambio, maxlag(6)
n pperron ln_cambio

n _print "*************** Taxa de Juros SELIC ****************"
n dfgls ln_selic, maxlag(6)
n pperron ln_selic

n _print "*************** PIB Inflacionado (IGP-DI) ****************"
n dfgls ln_pibinfl, maxlag(6)
n pperron ln_pibinfl

n _print "*************** Índice de Commodities - Brasil (IC-Br) ****************"
n dfgls ln_icbr, maxlag(6)
n pperron ln_icbr

n _print "*******************************************************"
// n block_prompt 1

n _print "------- TESTES CORRIGIDOS: DF-GLS, PP -------" 

n _print "*************** IPCA ****************"
n dfgls d.ln_ipca, maxlag(6)
n pperron d.ln_ipca

n _print "*************** Taxa de Câmbio (PTAX) ****************"
n dfgls d.ln_cambio, maxlag(6)
n pperron d.ln_cambio

n _print "*************** Taxa de Juros SELIC ****************"
n dfgls d.ln_selic, maxlag(6)
n pperron d.ln_selic

n _print "*************** PIB Inflacionado (IGP-DI) ****************"
n dfgls d.ln_pibinfl, maxlag(6)
n pperron d.ln_pibinfl

n _print "*************** Índice de Commodities - Brasil (IC-Br) ****************"
n dfgls d.ln_icbr, maxlag(6)
n pperron d.ln_icbr

n _print "*******************************************************"
// n block_prompt 1



n _print "------- Modelo VAR -------" 

n _print "*************** AIC, BIC, HQIC ****************"
n varsoc d.ln_ipca d.ln_cambio d.ln_selic d.ln_pibinfl d.ln_icbr

n _print "*************** IRF ****************"
n varbasic d.ln_ipca d.ln_cambio d.ln_selic d.ln_pibinfl d.ln_icbr, lags(1 2 3 4) step(12)
irf set "_varbasic.irf"

irf graph irf, irf(varbasic) impulse(D.ln_pibinfl D.ln_icbr) response(D.ln_ipca)

}
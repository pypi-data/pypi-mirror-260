# -*- coding: UTF-8 -*-
# Copyright 2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Febelfin Bank Transaction Code designations.

See :doc:`/specs/b2c`.


"""
from lino.api import _

DESCRIPTIONS = {
    '0101':
    _("Individual transfer order"),
    '0102':
    _("Individual transfer order initiated by the bank"),
    '0103':
    _("Standing order"),
    '0105':
    _("Payment of wages, etc."),
    '0107':
    _("Collective transfer"),
    '0113':
    _("Transfer from your account"),
    '0117':
    _("Financial centralisation"),
    '0137':
    _("Costs"),
    '0139':
    _("Your issue circular cheque"),
    '0140':
    _("Codes proper to each bank"),
    '0149':
    _("Cancellation or correction"),
    '0150':
    _("Transfer in your favour"),
    '0151':
    _("Transfer in your favour - initiated by the bank"),
    '0152':
    _("Payment in your favour"),
    '0154':
    _("Unexecutable transfer order"),
    '0160':
    _("Non-presented circular cheque"),
    '0162':
    _("Unpaid postal order"),
    '0164':
    _("Transfer to your account"),
    '0166':
    _("Financial centralization"),
    '0187':
    _("Reimbursement of costs"),
    '0190':
    _("Codes proper to each bank"),
    '0199':
    _("Cancellation or correction"),
    '0301':
    _("Payment of your cheque"),
    '0305':
    _("Payment of voucher"),
    '0309':
    _("Unpaid voucher"),
    '0311':
    _("Department store cheque"),
    '0315':
    _("Your purchase bank cheque"),
    '0317':
    _("Your certified cheque"),
    '0337':
    _("Cheque-related costs"),
    '0338':
    _("Provisionally unpaid"),
    '0340':
    _("Codes proper to each bank"),
    '0349':
    _("Cancellation or correction"),
    '0352':
    _("First credit of cheques, vouchers, luncheon vouchers, "
      "postal orders, credit under usual reserve"),
    '0358':
    _("Remittance of cheques, vouchers, etc. credit after collection"),
    '0360':
    _("Reversal of voucher"),
    '0362':
    _("Reversal of cheque"),
    '0363':
    _("Second credit of unpaid cheque"),
    '0366':
    _("Remittance of cheque by your branch-credit "
      "under usual reserve"),
    '0387':
    _("Reimbursement of cheque-related costs"),
    '0390':
    _("Codes proper to each bank"),
    '0399':
    _("Cancellation or correction"),
    '0401':
    _("Loading a GSM card"),
    '0402':
    _("Payment by means of a payment card within the Eurozone"),
    '0403':
    _("Settlement credit cards"),
    '0404':
    _("Cash withdrawal from an ATM"),
    '0405':
    _("Loading Proton"),
    '0406':
    _("Payment with tank card"),
    '0407':
    _("Payment by GSM"),
    '0408':
    _("Payment by means of a payment card outside the Eurozone"),
    '0437':
    _("Costs"),
    '0440':
    _("Codes proper to each bank"),
    '0449':
    _("Cancellation or correction"),
    '0450':
    _("Credit after a payment at a terminal"),
    '0451':
    _("Unloading Proton"),
    '0452':
    _("Loading GSM cards"),
    '0453':
    _("Cash deposit at an ATM"),
    '0455':
    _("Income from payments by GSM"),
    '0468':
    _("Credit after Proton payments"),
    '0487':
    _("Reimbursement of costs"),
    '0490':
    _("Codes proper to each bank"),
    '0499':
    _("Cancellation or correction"),
    '0501':
    _("Payment"),
    '0503':
    _("Unpaid debt"),
    '0505':
    _("Reimbursement"),
    '0537':
    _("Costs"),
    '0540':
    _("Codes proper to each institution"),
    '0549':
    _("Cancellation or correction"),
    '0550':
    _("Credit after collection"),
    '0552':
    _("Credit under usual reserve"),
    '0554':
    _("Reimbursement"),
    '0556':
    _("Unexecutable reimbursement"),
    '0558':
    _("Reversal"),
    '0587':
    _("Reimbursement of costs"),
    '0590':
    _("Codes proper to each bank"),
    '0599':
    _("Cancellation or correction"),
    '0701':
    _("Payment commercial paper"),
    '0705':
    _("Commercial paper claimed back"),
    '0706':
    _("Extension of maturity date"),
    '0707':
    _("Unpaid commercial paper"),
    '0708':
    _("Payment in advance"),
    '0709':
    _("Agio on supplier's bill"),
    '0737':
    _("Costs related to commercial paper"),
    '0739':
    _("Return of an irregular bill of exchange"),
    '0740':
    _("Codes proper to each bank"),
    '0749':
    _("Cancellation or correction"),
    '0750':
    _("Remittance of commercial paper-credit after collection"),
    '0752':
    _("Remittance of commercial paper-credit under usual reserve"),
    '0754':
    _("Remittance of commercial paper for discount"),
    '0756':
    _("Remittance of supplier's bill with guarantee"),
    '0758':
    _("Remittance of supplier's bill without guarantee"),
    '0787':
    _("Reimbursement of costs"),
    '0790':
    _("Codes proper to each bank"),
    '0799':
    _("Cancellation or correction"),
    '0901':
    _("Cash withdrawal"),
    '0905':
    _("Purchase of foreign bank notes"),
    '0907':
    _("Purchase of gold/pieces"),
    '0909':
    _("Purchase of petrol coupons"),
    '0913':
    _("Cash withdrawal by your branch or agents"),
    '0917':
    _("Purchase of fiscal stamps"),
    '0919':
    _("Difference in payment"),
    '0925':
    _("Purchase of traveller's cheque"),
    '0937':
    _("Costs"),
    '0940':
    _("Codes proper to each bank"),
    '0949':
    _("Cancellation or correction"),
    '0950':
    _("Cash payment"),
    '0952':
    _("Payment night safe"),
    '0958':
    _("Payment by your branch/agents"),
    '0960':
    _("Sale of foreign bank notes"),
    '0962':
    _("Sale of gold/pieces under usual reserve"),
    '0968':
    _("Difference in payment"),
    '0970':
    _("Sale of traveller's cheque"),
    '0987':
    _("Reimbursement of costs"),
    '0990':
    _("Codes proper to each bank"),
    '0999':
    _("Cancellation or correction"),
    '1101':
    _("Purchase of securities"),
    '1102':
    _("Tenders"),
    '1103':
    _("Subscription to securities"),
    '1104':
    _("Issues"),
    '1105':
    _("Partial payment subscription"),
    '1106':
    _("Share option plan -- exercising an option"),
    '1109':
    _("Settlement of securities"),
    '1111':
    _("Payable coupons/repayable securities"),
    '1113':
    _("Your repurchase of issue"),
    '1115':
    _("Interim interest on subscription"),
    '1117':
    _("Management fee"),
    '1119':
    _("Regularisation costs"),
    '1137':
    _("Costs"),
    '1140':
    _("Codes proper to each bank"),
    '1149':
    _("Cancellation or correction"),
    '1150':
    _("Sale of securities"),
    '1151':
    _("Tender"),
    '1152':
    _("Payment of coupons from a deposit or settlement of coupons "
      "delivered over the counter - credit under usual reserve"),
    '1158':
    _("Repayable securities from a deposit or delivered at the "
      "counter -- credit under usual reserve"),
    '1162':
    _("Interim interest on subscription When reimbursed separately "
      "to the subscriber"),
    '1164':
    _("Your issue"),
    '1166':
    _("Retrocession of issue commission"),
    '1168':
    _("Compensation for missing coupon"),
    '1170':
    _("Settlement of securities"),
    '1187':
    _("Reimbursement of costs"),
    '1190':
    _("Codes proper to each bank"),
    '1199':
    _("Cancellation or correction"),
    '1301':
    _("Short-term loan"),
    '1302':
    _("Long-term loan"),
    '1305':
    _("Settlement of fixed advance"),
    '1307':
    _("Your repayment instalment credits"),
    '1311':
    _("Your repayment mortgage loan"),
    '1313':
    _("Settlement of bank acceptances"),
    '1315':
    _("Your repayment hire-purchase and similar claims"),
    '1319':
    _("Documentary import credits"),
    '1321':
    _("Other credit applications"),
    '1337':
    _("Credit-related costs"),
    '1340':
    _("Codes proper to each bank"),
    '1349':
    _("Cancellation or correction"),
    '1350':
    _("Settlement of instalment credit"),
    '1354':
    _("Fixed advance -- capital and interest"),
    '1355':
    _("Fixed advance -- interest only"),
    '1356':
    _("Subsidy"),
    '1360':
    _("Settlement of mortgage loan"),
    '1362':
    _("Term loan"),
    '1368':
    _("Documentary export credits"),
    '1370':
    _("Settlement of discount bank acceptance"),
    '1387':
    _("Reimbursement of costs"),
    '1390':
    _("Codes proper to each bank"),
    '1399':
    _("Cancellation or correction"),
    '3001':
    _("Spot purchase of foreign exchange"),
    '3003':
    _("Forward purchase of foreign exchange"),
    '3005':
    _("Capital and/or interest term investment"),
    '3033':
    _("Value (date) correction"),
    '3037':
    _("Costs"),
    '3039':
    _("Undefined transaction"),
    '3040':
    _("Codes proper to each bank"),
    '3049':
    _("Cancellation or correction"),
    '3050':
    _("Spot sale of foreign exchange"),
    '3052':
    _("Forward sale of foreign exchange"),
    '3054':
    _("Capital and/or interest term investment"),
    '3055':
    _("Interest term investment"),
    '3083':
    _("Value (date) correction"),
    '3087':
    _("Reimbursement of costs"),
    '3089':
    _("Undefined transaction"),
    '3090':
    _("Codes proper to each bank"),
    '3099':
    _("Cancellation or correction"),
    '3501':
    _("Closing"),
    '3537':
    _("Costs"),
    '3540':
    _("Codes proper to each bank"),
    '3549':
    _("Cancellation or correction"),
    '3550':
    _("Closing"),
    '3587':
    _("Reimbursement of costs"),
    '3590':
    _("Codes proper to each bank"),
    '3599':
    _("Cancellation or correction"),
    '4101':
    _("Transfer"),
    '4103':
    _("Standing order"),
    '4105':
    _("Collective payments of wages"),
    '4107':
    _("Collective transfers"),
    '4113':
    _("Transfer from your account"),
    '4117':
    _("Financial centralisation (debit)"),
    '4137':
    _("Costs relating to outgoing foreign transfers and "
      "non-SEPA transfers"),
    '4138':
    _("Costs relating to incoming foreign and non-SEPA transfers"),
    '4140':
    _("Codes proper to each bank"),
    '4149':
    _("Cancellation or correction"),
    '4150':
    _("Transfer"),
    '4164':
    _("Transfer to your account"),
    '4166':
    _("Financial centralisation (credit)"),
    '4187':
    _("Reimbursement of costs"),
    '4190':
    _("Codes proper to each bank"),
    '4199':
    _("Cancellation or correction"),
    '4301':
    _("Payment of a foreign cheque"),
    '4307':
    _("Unpaid foreign cheque"),
    '4315':
    _("Purchase of an international bank cheque"),
    '4337':
    _("Costs relating to payment of foreign cheques"),
    '4340':
    _("Codes proper to each bank"),
    '4349':
    _("Cancellation or correction"),
    '4352':
    _("Remittance of foreign cheque credit under usual reserve"),
    '4358':
    _("Remittance of foreign cheque credit after collection"),
    '4362':
    _("Reversal of cheques"),
    '4387':
    _("Reimbursement of costs"),
    '4390':
    _("Codes proper to each bank"),
    '4399':
    _("Cancellation or correction"),
    '4701':
    _("Payment of foreign bill"),
    '4705':
    _("Bill claimed back"),
    '4706':
    _("Extension"),
    '4707':
    _("Unpaid foreign bill"),
    '4711':
    _("Payment documents abroad"),
    '4713':
    _("Discount foreign supplier's bills"),
    '4714':
    _("Warrant fallen due"),
    '4737':
    _("Costs relating to the payment of a foreign bill"),
    '4740':
    _("Codes proper to each bank"),
    '4749':
    _("Cancellation or correction"),
    '4750':
    _("Remittance of foreign bill credit after collection"),
    '4752':
    _("Remittance of foreign bill credit under usual reserve"),
    '4754':
    _("Discount abroad"),
    '4756':
    _("Remittance of guaranteed foreign supplier's bill"),
    '4758':
    _("Idem without guarantee"),
    '4760':
    _("Remittance of documents abroad - credit under usual reserve"),
    '4762':
    _("Remittance of documents abroad - credit after collection"),
    '4764':
    _("Warrant"),
    '4787':
    _("Reimbursement of costs"),
    '4790':
    _("Codes proper to each bank"),
    '4799':
    _("Cancellation or correction"),
    '8002':
    _("Costs relating to electronic output"),
    '8004':
    _("Costs for holding a documentary cash credit"),
    '8006':
    _("Damage relating to bills and cheques"),
    '8007':
    _("Insurance costs"),
    '8008':
    _("Registering compensation for savings accounts"),
    '8009':
    _("Postage"),
    '8010':
    _("Purchase of Smartcard"),
    '8011':
    _("Fees and commissions charged separately"),
    '8012':
    _("Costs for opening a bank guarantee"),
    '8013':
    _("Renting of safes"),
    '8014':
    _("Handling costs instalment credit"),
    '8015':
    _("Night safe"),
    '8016':
    _("Bank confirmation to revisor or accountant"),
    '8017':
    _("Charge for safe custody"),
    '8018':
    _("Trade information"),
    '8019':
    _("Special charge for safe custody"),
    '8020':
    _("Drawing up a certificate"),
    '8021':
    _("Pay-packet charges"),
    '8022':
    _("Management/custody"),
    '8023':
    _("Research costs"),
    '8024':
    _("Participation in and management of interest refund system"),
    '8025':
    _("Renting of direct debit box"),
    '8026':
    _("Travel insurance premium"),
    '8027':
    _("Subscription fee"),
    '8029':
    _("Information charges"),
    '8031':
    _("Writ service fee"),
    '8033':
    _("Miscellaneous fees and commissions"),
    '8035':
    _("Costs"),
    '8037':
    _("Access right to database"),
    '8039':
    _("Surety fee"),
    '8041':
    _("Research costs"),
    '8043':
    _("Printing of forms"),
    '8045':
    _("Documentary credit charges"),
    '8047':
    _("Charging fees for transactions"),
    '8049':
    _("Cancellation or correction"),
    '8099':
    _("Cancellation or correction"),
}


def code2desc(c):
    """Return the description of the given code."""
    return DESCRIPTIONS.get(c, c)

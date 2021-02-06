import sys
sys.path.append('../../')

import os
import json
import unittest
from unittest import mock

with mock.patch.dict('os.environ', {'AWS_REGION': 'us-east-1', 'EMAIL_DOMAIN': 'mock-domain', 'EMAIL_ADDRESS': 'mock-address'}):
  from parse_email_and_notify.app import lambda_handler

def mocked_get_file_from_s3_delivery_failure(bucket_key, bucket_name, bucket_region):
  return """
            Return-Path: <>
            Received: from a14-86.smtp-out.amazonses.com (a14-86.smtp-out.amazonses.com [54.240.14.86])
            by inbound-smtp.us-east-1.amazonaws.com with SMTP id 5e80t24a0jg9pdfa0mqcdr913btr0bukk325cq01
            for myemail@sesdomain.com;
            Sun, 17 Jan 2021 11:52:22 +0000 (UTC)
            X-SES-Spam-Verdict: PASS
            X-SES-Virus-Verdict: PASS
            Received-SPF: none (spfCheck: 54.240.14.86 is neither permitted nor denied by domain of a14-86.smtp-out.amazonses.com) client-ip=54.240.14.86; envelope-from=postmaster@a14-86.smtp-out.amazonses.com; helo=a14-86.smtp-out.amazonses.com;
            Authentication-Results: amazonses.com;
            spf=none (spfCheck: 54.240.14.86 is neither permitted nor denied by domain of a14-86.smtp-out.amazonses.com) client-ip=54.240.14.86; envelope-from=postmaster@a14-86.smtp-out.amazonses.com; helo=a14-86.smtp-out.amazonses.com;
            dkim=pass header.i=@amazonses.com;
            dmarc=permerror;
            X-SES-RECEIPT: AEFBQUFBQUFBQUFHaG80allUNGdFeGttY0tsck1MQVVydy9HczVsUEVldTQ2bVNvWm13Q1BSTkwzZXNWWWQ2b2lvSk1aUFc1YXQ5TlcyTzFHN0hCM1FMbkRadDNiY2pjblNMOWtSakVMa0FKbzd1amh0cVFvMGVCZVpDR1lLTUltRFdLQVkwTGRRZXZJcGVybnV4YkorZnJkc2tXNHN4TksrS0lqZEVkdnpLUStvenRiSk4rK1FneFZmblFKNDlsOVpWb2FodEg0RFltUVREa1FtRVFWOUQySDdEdWd4MS81ZWVZK3J6U3B6NmovNVl0SkhsLzhpaGpUaHQzN0dPSGFoa01UTG4rL3VweEpkTEJaRk1XNnFjY1lJL29YekRGdA==
            X-SES-DKIM-SIGNATURE: a=rsa-sha256; q=dns/txt; b=R+q2Xpd39MJEe7syUsDvYHPqmaKzfZ/FegEjqlZWijBO45lJqRUqecgcuu5aBsPdyUrpNfF4fqHcJo/Ue8k49giFYpwwB6YWn1DCo1fINZmAJluxaDuji71iU9A6ZlsbdJ106CJ2QnQ1o+n5t65finRB2FXTt7oCsrFdzroxzQA=; c=relaxed/simple; s=224i4yxa5dv7c2xz3womw6peuasteono; d=amazonses.com; t=1610884343; v=1; bh=1GqyKTlGVWzqgqt2kdClvDj0oykyrcWMo9otFF6dISM=; h=From:To:Cc:Bcc:Subject:Date:Message-ID:MIME-Version:Content-Type:X-SES-RECEIPT;
            DKIM-Signature: v=1; a=rsa-sha256; q=dns/txt; c=relaxed/simple;
              s=224i4yxa5dv7c2xz3womw6peuasteono; d=amazonses.com; t=1610884342;
              h=Date:From:To:Message-ID:Subject:MIME-Version:Content-Type:Feedback-ID;
              bh=1GqyKTlGVWzqgqt2kdClvDj0oykyrcWMo9otFF6dISM=;
              b=hWhGCXLTbIjuvP/fCIknjhyFr631Wk8uhWOXRVbBKFR9JiwLA0V8tdW5VDOepU9J
              rm+puJhvdgilOiO6fTc0GQIpfmDe1vTzh4u/zNuoHWyTsTaUDIa6vi6uwpGspqrYhYR
              rTlS2lze0APuVWioAN98+aZCVw9XzQwujNqBnZWY=
            Date: Sun, 17 Jan 2021 11:52:22 +0000
            From: MAILER-DAEMON@amazonses.com
            To: My SES Domain Email <myemail@sesdomain.com>
            Message-ID: <010001771030627d-3007cb08-d15c-4031-9e78-a9f66d69b2da-000000@email.amazonses.com>
            Subject: Delivery Status Notification (Failure)
            MIME-Version: 1.0
            Content-Type: multipart/report; 
              boundary="----=_Part_5909269_2113273023.1610884342420"; 
              report-type=delivery-status
            X-SES-Outgoing: 2021.01.17-54.240.14.86
            Feedback-ID: 1.us-east-1.D1mWDvwUtiZJdKFArGKkGBe9wfRCdAX2ofq5lyeEo20=:AmazonSES

            ------=_Part_5909269_2113273023.1610884342420
            Content-Type: text/plain; charset=us-ascii
            Content-Transfer-Encoding: 7bit
            Content-Description: Notification

            An error occurred while trying to deliver the mail to the following recipients:
            deliveryfailure@thisemail.com
            ------=_Part_5909269_2113273023.1610884342420
            Content-Type: message/delivery-status
            Content-Transfer-Encoding: 7bit
            Content-Description: Delivery Status Notification

            Reporting-MTA: dsn; a8-61.smtp-out.amazonses.com

            Action: failed
            Final-Recipient: rfc822; deliveryfailure@thisemail.com
            Diagnostic-Code: smtp; 554 4.4.7 Message expired: unable to deliver in 840 minutes.<451 4.7.651 The mail server [54.240.8.61] has been temporarily rate limited due to IP reputation. For e-mail delivery information, see https://postmaster.live.com (S844) [AM7EUR06FT034.eop-eur06.prod.protection.outlook.com]>
            Status: 4.4.7


            ------=_Part_5909269_2113273023.1610884342420
            Content-Type: message/rfc822
            Content-Description: Undelivered Message

            From: My SES Domain Email <myemail@sesdomain.com>
            To: deliveryfailure@thisemail.com
            Subject: Daily vocab word - Jan. 16, 2021
            MIME-Version: 1.0
            Content-Type: text/html; charset=UTF-8
            Content-Transfer-Encoding: quoted-printable
            Message-ID: <010001770cc8cfa3-793a9c12-1945-4a17-a44a-4191cf0c1a90-000000@email.amazonses.com>
            Date: Sat, 16 Jan 2021 20:00:22 +0000
            X-SES-Outgoing: 2021.01.16-54.240.8.61
            Feedback-ID: 1.us-east-1.Bo0g5qGdW7jOhmyX6oEtn94mfviFLj123hIk4/NRWpc=:AmazonSES
            DKIM-Signature: v=1; a=rsa-sha256; q=dns/txt; c=relaxed/simple;
              s=224i4yxa5dv7c2xz3womw6peuasteono; d=amazonses.com; t=1610827223;
              h=From:To:Subject:MIME-Version:Content-Type:Content-Transfer-Encoding:Message-ID:Date:Feedback-ID;
              bh=UMJ2QVfWadi36+J9ufGaXtbyHukFUIREIi8l+zkEL7s=;
              b=PFztvbDHT56ncfywIn1h0/mKj0KSG8u3hNAKLXRS30gQpdP7hWWhwJ4zRrQg+8xR
              0gJjBKoY5tXhYAhmpT9aBiDsw5njOcmv8gQ6h1Qd5cY7mctjNMh8Qh51HdOJ+k1/IWb
              BSor1O2bqK8RXnb793lTlF47UIs9Gnq2H5rJvIjQ=
            DKIM-Signature: v=1; a=rsa-sha256; q=dns/txt; c=relaxed/simple;
              s=aqehp37lgdq2eyac5bd5wsyns5yuswqf; d=My SES Domain Email.com;
              t=1610827223;
              h=From:To:Subject:MIME-Version:Content-Type:Content-Transfer-Encoding:Message-ID:Date;
              bh=UMJ2QVfWadi36+J9ufGaXtbyHukFUIREIi8l+zkEL7s=;
              b=ySC5R8mJICxqXlx9eJAxUJPOdmu5FL3qMhERe2hdJ3KKbKOFnwAZHq2A4nFR6MJk
              FjNRfpUPI2QMzvHOyrGIB3QMHC+v71XdVE+A7mc1SlFyLL5ey2edE3Ke3v+ANpk1Ol4
              WK/1lt80H86ut5+2IMndKoA6yaEB3i59DRM8jdYw=

            ------=_Part_5909269_2113273023.1610884342420--
          """

def mocked_get_file_from_s3_delivery_error(bucket_key, bucket_name, bucket_region):
  return """
            Return-Path: <>
            Received: from m12-53.163.com (163.mxmail.netease.com [220.181.12.53])
            by inbound-smtp.us-east-1.amazonaws.com with SMTP id 5hb2bs1g6m0qnbsmk3m0csgl4j2osbk1gg3pbao1
            for cvxq@mydomain.com;
            Sat, 23 Jan 2021 13:17:04 +0000 (UTC)
            X-SES-Spam-Verdict: PASS
            X-SES-Virus-Verdict: PASS
            Received-SPF: none (spfCheck: 220.181.12.53 is neither permitted nor denied by domain of 163.mxmail.netease.com) client-ip=220.181.12.53; envelope-from=postmaster@163.mxmail.netease.com; helo=163.mxmail.netease.com;
            Authentication-Results: amazonses.com;
            spf=none (spfCheck: 220.181.12.53 is neither permitted nor denied by domain of 163.mxmail.netease.com) client-ip=220.181.12.53; envelope-from=postmaster@163.mxmail.netease.com; helo=163.mxmail.netease.com;
            dmarc=permerror;
            X-SES-RECEIPT: AEFBQUFBQUFBQUFFcXBJa09wZkRrdkJ0M3lvdEd1VkFsUEwrUkVqTUV6TlFxMTg2QUhYdzY1NGJiZTBsek01clVjUHVBR1hqQ2V0OFBRcG9mdUV1a2l1OVpRbWV3VnRqUWJQb1VjenNoVlFUWGFBdGZoY1BPWGkvNTRRUnk3WnVEc1ZrVzhWc2JncmdoSUtVZExBZURpdkZtUFUycU94REFOTjNBMGZQQU1NK3U0aE1HN2xTODJHYVBwT0xIUUx3c1pqS2JrTDA1Z09hVGgyZUF6UHdqVlYvaHR5TlNBM2pqMC94U3RLcXQ4QzZ5NGpEMFFISXRYbjluaXhtb1BjTm5YRGQyR2RhYkYvcjZmcXlYdFpqRGlEWE1leDZjZUxDcA==
            X-SES-DKIM-SIGNATURE: a=rsa-sha256; q=dns/txt; b=QQ/lyQNhvRyFXOF9iBfeD0uc0HDGU6Jtfmc8DTNsrNFPUoft1eqAkIRLXaXqecAnMSAbBvMkllPUavOvA7tER2Zj7jC3cY2vqP+CZbVZUK4WN64hrqdlDMPoZ6cbD0ix4fmvrzeH70JMA4Sv/9QKsV54bMWlGxLwKERk/ijJZuc=; c=relaxed/simple; s=224i4yxa5dv7c2xz3womw6peuasteono; d=amazonses.com; t=1611407829; v=1; bh=ZE5kpW1kom4u+ssEHtUITkIOERfYiaaC5GBKBlcZ5GQ=; h=From:To:Cc:Bcc:Subject:Date:Message-ID:MIME-Version:Content-Type:X-SES-RECEIPT;
            From: Postmaster@163.com
            To: cvxq@mydomain.com
            Subject: =?gb2312?B?z7XNs83L0MU=?=
            MIME-Version: 1.0
            Content-Type: Multipart/report;
              report-type=delivery-status;
              boundary="------------Boundary-00=_182E1KSR955BHUC3LVC0"
            Message-Id: <600C21C1.92BF04.01244@163mx3.163.com>
            Date: Sat, 23 Jan 2021 21:16:49 +0800 (CST)
            Delivered-To: ych008stc@163.comych008stc@163.com
            X-CM-Original-Message-ID: 12b5e9fd-beef-407d-aaaf-8de99694d40f
            X-Mailer: Coremail MTA server
            X-CM-TRANSID:NcCowACn05nAIQxgsoW+DQ--.32572S2.B29985



            --------------Boundary-00=_182E1KSR955BHUC3LVC0
            MIME-Version: 1.0
            Content-Type: Multipart/Alternative;
              boundary="------------Boundary-00=_182ER60R955BHUC3LVC0"


            --------------Boundary-00=_182ER60R955BHUC3LVC0
            Content-Type: Text/Plain;
              charset="gb2312"
            Content-Transfer-Encoding: base64
            Content-Description: Notification

            safHuKOsxPq1xNPKvP6xu83Lu9jAtMHLoa2hrQ0KICAgICAg1K3Tyrz+0MXPoqO6DQogICAgICAg
            ICAgICDKsSAgvOQgMjAyMS0wMS0yMyAyMToxMzoyOSAgDQogICAgICAgICAgICDW9yAgzOIgxOO6
            wyAgDQogICAgICAgICAgICDK1bz+yMsgeWNoMDA4c3RjQDE2My5jb20gIA0KICAgICANCiAgICAg
            IM3L0MXUrdLyo7oNCiAgICAgICAgICAgIMCsu/jTyrz+yMPTys/k0KHS17rct7PQxKOsz9bU2sT6
            t6LLzbXE08q8/rG7u7PSyc6qysfArLv408q8/qOsvty++L3TytWhow0KICAgICAgICAgICAg06LO
            xMu1w/c6cmVqZWN0ZWQgYnkgc3lzdGVtIA0KDQogICAgICC9qNLpveK+9re9sLijug0KICAgICAg
            ICAgICAg08qy7tCh0tfOwtywzOHKvqO6vajS6cT6wszJq7XYyrnTw9PKz+SjrMfrysq1sdDeuMSx
            6szius3E2sjdo6zU2bOiytS3osvNoaMNCg0KLS0tLS0tLS0tLS0tLS0tLQ0KVGhpcyBtZXNzYWdl
            IGlzIGdlbmVyYXRlZCBieSBDb3JlbWFpbC4NCsT6ytW1vbXEysfAtNfUIENvcmVtYWlsINeo0rXT
            yrz+z7XNs7XE0MW8/i4NCg0K

            --------------Boundary-00=_182ER60R955BHUC3LVC0
            Content-Type: Text/HTML;
              charset="gb2312"
            Content-Transfer-Encoding: base64
            Content-Description: Notification

            PCEtLSBzYXZlZCBmcm9tIHVybD0oMDAyMilodHRwOi8vaW50ZXJuZXQuZS1tYWlsIC0tPiANCjxo
            dG1sPiANCjxoZWFkPiANCjxtZXRhIGh0dHAtZXF1aXY9IkNvbnRlbnQtVHlwZSIgY29udGVudD0i
            dGV4dC9odG1sOyBjaGFyc2V0PWdiMjMxMiIgLz4gDQo8bWV0YSBuYW1lPSJLZXl3b3JkcyIgY29u
            dGVudD0iIiAvPiANCjxtZXRhIG5hbWU9IkRlc2NyaXB0aW9uIiBjb250ZW50PSIiIC8+IA0KPHRp
            dGxlPjwvdGl0bGU+IA0KIA0KPHN0eWxlIHR5cGU9InRleHQvY3NzIj4gDQo8IS0tDQogDQpib2R5
            LGRpdixkbCxkdCxkZCxoMSxoMixoMyxoNCxoNSxoNixwcmUsZm9ybSxmaWVsZHNldCxpbnB1dCx0
            ZXh0YXJlYSxwLGJsb2NrcXVvdGUsdGgsdGR7cGFkZGluZzowOyBtYXJnaW46MDsgfQ0KZmllbGRz
            ZXQsaW1ne2JvcmRlcjowOyB9DQp0YWJsZXtib3JkZXItY29sbGFwc2U6Y29sbGFwc2U7IGJvcmRl
            ci1zcGFjaW5nOjA7IH0NCm9sLHVse30NCmFkZHJlc3MsY2FwdGlvbixjaXRlLGNvZGUsZGZuLGVt
            LHN0cm9uZyx0aCx2YXJ7Zm9udC13ZWlnaHQ6bm9ybWFsOyBmb250LXN0eWxlOm5vcm1hbDsgfQ0K
            Y2FwdGlvbix0aHt0ZXh0LWFsaWduOmxlZnQ7IH0NCmgxLGgyLGgzLGg0LGg1LGg2e2ZvbnQtd2Vp
            Z2h0OmJvbGQ7IGZvbnQtc2l6ZToxMDAlOyB9DQpxOmJlZm9yZSxxOmFmdGVye2NvbnRlbnQ6Jyc7
            IH0NCmFiYnIsYWNyb255bXtib3JkZXI6MDsgfQ0KIA0KYTpsaW5rLGE6dmlzaXRlZHt9DQphOmhv
            dmVye30NCiANCi5CZHl7Zm9udC1zaXplOjE0cHg7IGZvbnQtZmFtaWx5OnZlcmRhbmEsQXJpYWws
            SGVsdmV0aWNhLHNhbnMtc2VyaWY7IHBhZGRpbmc6MjBweDt9DQpoMXtmb250LXNpemU6MjRweDsg
            Y29sb3I6I2NkMDAyMTsgcGFkZGluZy1ib3R0b206MzBweDt9DQpwe30NCiANCi5UYl9tV3B7Ym9y
            ZGVyOjFweCBzb2xpZCAjZGRkOyBib3JkZXItcmlnaHQ6bm9uZTsgYm9yZGVyLWJvdHRvbTpub25l
            OyB0YWJsZS1sYXlvdXQ6Zml4ZWQ7fQ0KICAgIC5UYl9tV3AgdGgsLlRiX21XcCB0ZHtib3JkZXIt
            cmlnaHQ6MXB4IHNvbGlkICNkZGQ7IGJvcmRlci1ib3R0b206MXB4IHNvbGlkICNkZGQ7IHBhZGRp
            bmc6OHB4IDRweDt9DQogICAgLlRiX21XcCB0aHtmb250LXNpemU6MTRweDsgdGV4dC1hbGlnbjpy
            aWdodDsgd2lkdGg6MTMwcHg7IGZvbnQtd2VpZ2h0OmJvbGQ7IGJhY2tncm91bmQ6I2Y2ZjZmNjsg
            Y29sb3I6IzY2Njt9DQogICAgLlRiX21XcCB0ZHtmb250LXNpemU6MTRweDsgcGFkZGluZy1sZWZ0
            OjEwcHg7IHdvcmQtYnJlYWs6YnJlYWstYWxsO30NCiANCi5UYl9taVdweyBtYXJnaW4tdG9wOi0y
            cHg7IG1hcmdpbi1sZWZ0Oi0xcHg7IGZsb2F0OmxlZnQ7IHRhYmxlLWxheW91dDpmaXhlZDt9DQog
            ICAgLlRiX21pV3AgdGgsLlRiX21pV3AgdGR7Ym9yZGVyLWxlZnQ6MXB4IHNvbGlkICNlZWU7IGJv
            cmRlci10b3A6MXB4IHNvbGlkICNlZWU7IGJvcmRlci1yaWdodDpub25lOyBib3JkZXItYm90dG9t
            Om5vbmU7IGZvbnQtc2l6ZToxMnB4O2xpbmUtaGVpZ2h0OjE4cHh9DQogICAgLlRiX21pV3AgdGh7
            d2lkdGg6NjhweDsgYmFja2dyb3VuZDojZjhmOGY4O2xpbmUtaGVpZ2h0OjE4cHh9DQogDQoudHJf
            TWl7fQ0KICAgIC50cl9NaSB0aHt9DQogICAgLnRyX01pIHRke30NCiANCi50cl9Sent9DQogICAg
            LnRyX1J6IHRoe30NCiAgICAudHJfUnogdGR7IGJhY2tncm91bmQ6I2ZmZjRmNjt9DQogICAgICAg
            IC50cl9SeiAuaW5mb1R0eyBjb2xvcjojY2QwMDIxOyBmb250LXdlaWdodDpib2xkOyBsaW5lLWhl
            aWdodDoxOHB4O30NCiAgICAgICAgLnRyX1J6IC5pbmZvRGNyeyBwYWRkaW5nLXRvcDo0cHg7IGNv
            bG9yOiM5OTk7IGxpbmUtaGVpZ2h0OjE4cHg7fQ0KIA0KLnRyX1Nye30NCiAgICAudHJfU3IgdGh7
            fQ0KICAgIC50cl9TciB0ZHtiYWNrZ3JvdW5kOiNmNGZmZjQ7fQ0KIA0KLnVsX2xzdFdwe21hcmdp
            bi1sZWZ0Oi0yMHB4O30NCi51bF9sc3R7cGFkZGluZy10b3A6MHB4OyBwYWRkaW5nLWJvdHRvbTow
            cHg7IG1hcmdpbi10b3A6NnB4OyBtYXJnaW4tYm90dG9tOjZweDt9DQoudWxfbHN0IGxpe3BhZGRp
            bmctdG9wOjNweDsgcGFkZGluZy1ib3R0b206M3B4O30NCiANCiANCiANCiANCi0tPg0KPC9zdHls
            ZT4gDQogDQo8L2hlYWQ+IA0KIA0KPGJvZHkgY2xhc3M9IkJkeSI+IA0KIA0KPGgxPrGnx7ijrMT6
            tcTTyrz+sbvNy7vYwLTBy6Gtoa08L2gxPiANCiANCjxkaXYgY2xhc3M9IkNvbiI+IA0KPHRhYmxl
            IHdpZHRoPSIxMDAlIiBib3JkZXI9IjAiIGNlbGxzcGFjaW5nPSIwIiBjZWxscGFkZGluZz0iMCIg
            Y2xhc3M9IlRiX21XcCI+IA0KICAgIA0KICAgIDwhLS0g1K3Tyrz+0MXPoiAtLT4gDQogICAgPHRy
            IGNsYXNzPSJ0cl9NaSI+IA0KICAgICAgICA8dGggbm93cmFwPtSt08q8/tDFz6KjujwvdGg+IA0K
            ICAgICAgICA8dGQgc3R5bGU9InBhZGRpbmc6MHB4OyBmb250LXNpemU6MXB4OyBsaW5lLWhlaWdo
            dDoxcHg7IG92ZXJmbG93OmhpZGRlbjsgdmVydGljYWwtYWxpZ246dG9wOyI+IA0KDQogICAgICAg
            ICAgICA8dGFibGUgd2lkdGg9IjEwMCUiIGJvcmRlcj0iMCIgY2VsbHNwYWNpbmc9IjAiIGNlbGxw
            YWRkaW5nPSIwIiBjbGFzcz0iVGJfbWlXcCI+IA0KICAgICAgICAgICAgICAgIDx0cj4gDQogICAg
            ICAgICAgICAgICAgICAgIDx0aCBub3dyYXA+yrGhobzko7o8L3RoPiANCiAgICAgICAgICAgICAg
            ICAgICAgPHRkIHN0eWxlPSJsaW5lLWhlaWdodDoxIj4yMDIxLTAxLTIzIDIxOjEzOjI5PC90ZD4g
            DQogICAgICAgICAgICAgICAgPC90cj4gDQqhoSAgICAgICAgICAgICAgICA8dHI+IA0KICAgICAg
            ICAgICAgICAgICAgICA8dGggbm93cmFwPtb3oaHM4qO6PC90aD4gDQogICAgICAgICAgICAgICAg
            ICAgIDx0ZCBzdHlsZT0ibGluZS1oZWlnaHQ6MSI+xOO6wzwvdGQ+DQogICAgICAgICAgICAgICAg
            PC90cj4gDQogICAgICAgICAgICAgICAgPHRyPiANCiAgICAgICAgICAgICAgICAgICAgPHRoIG5v
            d3JhcD7K1bz+yMujujwvdGg+IA0KICAgICAgICAgICAgICAgICAgICA8dGQgc3R5bGU9ImxpbmUt
            aGVpZ2h0OjEiPnljaDAwOHN0Y0AxNjMuY29tPC90ZD4gDQogICAgICAgICAgICAgICAgPC90cj4g
            DQogICAgICAgICAgICAgICAgPHRyIHN0eWxlPSJkaXNwbGF5Om5vbmU7Ij48IS0tICAtLT4gDQog
            ICAgICAgICAgICAgICAgICAgIDx0aCBub3dyYXA+s62hocvNo7o8L3RoPiANCiAgICAgICAgICAg
            ICAgICAgICAgPHRkIHN0eWxlPSJsaW5lLWhlaWdodDoxIj54eHg8L3RkPiANCiAgICAgICAgICAg
            ICAgICA8L3RyPiANCiAgICAgICAgICAgICAgICA8dHIgc3R5bGU9ImRpc3BsYXk6bm9uZTsiPiAN
            CiAgICAgICAgICAgICAgICAgICAgPHRoIG5vd3JhcD7D3KGhy82jujwvdGg+PCEtLSAgLS0+IA0K
            ICAgICAgICAgICAgICAgICAgICA8dGQgc3R5bGU9ImxpbmUtaGVpZ2h0OjEiPnl5eTwvdGQ+IA0K
            ICAgICAgICAgICAgICAgIDwvdHI+IA0KICAgICAgICAgICAgPC90YWJsZT4gDQogICAgICAgICAg
            ICA8IS0tINSt08q8/tDFz6LB0LHtIEVuZCAtLT4gDQogDQogDQogDQogDQogICAgICAgIDwvdGQ+
            IA0KICAgIDwvdHI+IA0KIA0KICAgIDwhLS0gzcvQxdSt0vIgLS0+IA0KICAgIDx0ciBjbGFzcz0i
            dHJfUnoiPiANCiAgICAgICAgPHRoIG5vd3JhcD7Ny9DF1K3S8qO6PC90aD4gDQogICAgICAgIDx0
            ZD4gDQogICAgICAgICAgICA8IS0tIHdheWhvbWUgMjAwOS0zLTkgLS0+IA0KICAgICAgICAgICAg
            PGRpdiBjbGFzcz0iaW5mb1R0Ij7ArLv408q8/sjD08rP5NCh0te63Lez0MSjrM/W1NrE+reiy821
            xNPKvP6xu7uz0snOqsrHwKy7+NPKvP6jrL7cvvi908rVoaM8L2Rpdj4gDQogICAgICAgICAgICA8
            ZGl2IGNsYXNzPSJpbmZvRGNyIj7Tos7Ey7XD9zpyZWplY3RlZCZuYnNwO2J5Jm5ic3A7c3lzdGVt
            PC9kaXY+IA0KICAgICAgICA8L3RkPiANCiAgICA8L3RyPiANCiANCiAgICA8IS0tIL3ivva3vbC4
            IC0tPiANCiAgICA8dHIgY2xhc3M9InRyX1NyIj4gDQogICAgICAgIDx0aCBub3dyYXA+vajS6b3i
            vva3vbC4o7o8L3RoPiANCiAgICAgICAgPHRkPiANCiAgICAgICAgICAgIDxkaXYgY2xhc3M9InVs
            X2xzdFdwIj4gDQogICAgICAgICAgICA8dWwgY2xhc3M9InVsX2xzdCI+IA0KICAgICAgICAgICAg
            ICAgIDxsaT7TyrLu0KHS187C3LDM4cq+o7q9qNLpxPrCzMmrtdjKudPD08rP5KOsx+vKyrWx0N64
            xLHqzOK6zcTayN2jrNTZs6LK1Leiy82hozwvbGk+IA0KICAgICAgICAgICAgICAgIDxsaT7I57n7
            xPrT0Mbky/vNy9DFzsrM4qOsu7bTrc/yzfjS19PKvP7W0NDEPGEgaHJlZj0iaHR0cDovL2ZlZWRi
            YWNrLm1haWwuMTI2LmNvbS9hbnRpc3BhbS9yZXBvcnQucGhwPyZCb3VuY2VSZWFzb249cmVqZWN0
            ZWQlMjZuYnNwJTNCYnklMjZuYnNwJTNCc3lzdGVtJkJvdW5jZWRSY3B0PXljaDAwOHN0YyU0MDE2
            My5jb20mQ2x1c3RlcklEPTMuMzI0NTk5OTcmT3JnU3ViamVjdD0lQzQlRTMlQkElQzMmU2VuZERh
            dGU9MTYxMTQwNzYwOSZTZW5kZXI9Y3Z4cSU0MGVtc2hlYS5jb20mVHJhbnNJRD1OY0Nvd0FDbjA1
            bkFJUXhnc29XJTJCRFEtLS4zMjU3MlMyLkIyOTk4NSIgdGFyZ2V0PSJfYmxhbmsiPreiy83Ny9DF
            sai45jwvYT48L2xpPg0KICAgICAgICAgICAgICAgIDxsaT7I57n7xPrK1bW9tPPBv83L0MW2+LfH
            sb7Iy7LZ1/ejrL2o0unE+jxhIGhyZWY9Imh0dHBzOi8vcmVnLjE2My5jb20vc2V0aW5mby9DaGFu
            Z2VQd2RfMS5qc3AiIHRhcmdldD0iX2JsYW5rIj7C7cnP0N64xMPcwus8L2E+o6yyotTa08rP5M34
            0rOw5jxhIGhyZWY9Imh0dHA6Ly9jb3VudC5tYWlsLjE2My5jb20vc3RhdGlzdGljcy9pbmY3NnMu
            ZG8iIHRhcmdldD0iX2JsYW5rIiBzeXM9IjEiIGludGVyZmFjZT0iT3B0aW9uSW50ZXJmYWNlIiBw
            YXJhbT0iTGlua01vZHVsZS5vcHRpb25fYXV0aENvZGUiPtbYyei/zbuntsvK2siowus8L2E+IKGi
            PGEgaHJlZj0iaHR0cDovL2NvdW50Lm1haWwuMTYzLmNvbS9zdGF0aXN0aWNzL2luZjc2cy5kbyIg
            dGFyZ2V0PSJfYmxhbmsiIHN5cz0iMSIgaW50ZXJmYWNlPSJPcHRpb25JbnRlcmZhY2UiIHBhcmFt
            PSJMaW5rTW9kdWxlLnNlY29uZGF1dGgiPr+qxvS1x8K8tv60ztHp1qQ8L2E+oaM8L2xpPg0KICAg
            ICAgICAgICAgPC91bD4gDQogICAgICAgICAgICA8L2Rpdj4gICAgICAgIA0KICAgICAgICA8L3Rk
            PiANCiAgICA8L3RyPiANCg0KPC90YWJsZT4gDQogDQo8L2Rpdj4gDQogDQoNCjwhLS0gZm9vdGVy
            IC0tPg0KPHNwYW4+DQo8YnI+LS0tLS0tLS0tLS0tLS0tLTxicj5UaGlzIG1lc3NhZ2UgaXMgZ2Vu
            ZXJhdGVkIGJ5IENvcmVtYWlsLjxicj7E+srVtb21xMrHwLTX1CBDb3JlbWFpbCDXqNK108q8/s+1
            zbO1xNDFvP4uPGJyPjxicj4NCjwvc3Bhbj4NCjwvYm9keT4gDQo8L2h0bWw+DQo=

            --------------Boundary-00=_182ER60R955BHUC3LVC0--

            --------------Boundary-00=_182E1KSR955BHUC3LVC0
            Content-Type: Message/delivery-status
            Content-Description: Delivery error report

            Final-Recipient: rfc822; ych008stc@163.com
            Action: failed
            Status: 5.0.0
            Diagnostic-Code: SMTP; rejected by system
            --------------Boundary-00=_182E1KSR955BHUC3LVC0
            Content-Type: Message/Rfc822
            Content-Description: Undelivered Message
            Content-Transfer-Encoding: 8bit

            Received: from ndye.com (unknown [60.167.113.246])
              by mx3 (Coremail) with SMTP id NcCowACn05nAIQxgsoW+DQ--.32572S2;
              Sat, 23 Jan 2021 21:16:48 +0800 (CST)
            Received: from desktop ([127.0.0.1]) by localhost via TCP with ESMTPA; Sat, 23 Jan 2021 21:13:29 +0800
            Message-ID: 12b5e9fd-beef-407d-aaaf-8de99694d40f
            MIME-Version: 1.0
            Sender: "sophie"
            <cvxq@mydomain.com>
            From: "sophie"
            <gcut@mydomain.com>
            To: ych008stc@163.com
            Date: 23 Jan 2021 21:13:29 +0800
            Subject: =?utf-8?B?5L2g5aW9?=
            Content-Type: multipart/alternative;
            boundary=--boundary_3658080_51a0ee0b-d096-4c14-bb0c-c0b4f7d69726
            X-CM-TRANSID:NcCowACn05nAIQxgsoW+DQ--.32572S2
            Authentication-Results: mx3; spf=none smtp.mail=cvxq@mydomain.com;
            X-Coremail-Antispam: 1Uf129KBjDUn29KB7ZKAUJUUUUU529EdanIXcx71UUUUU7v73
              VFW2AGmfu7bjvjm3AaLaJ3UbIYCTnIWIevJa73UjIFyTuYvjxUyo7KDUUUU


            ----boundary_3658080_51a0ee0b-d096-4c14-bb0c-c0b4f7d69726
            Content-Type: text/plain; charset=utf-8
            Content-Transfer-Encoding: base64

            5pyJ5q2j6KeE5Y+R56Wo5Y+v5Lul5byA77yM5Lu35qC85LyY5oOg77yM6ZW/5pyf
            5pyJ5pWI77yM6ZyA6KaB5Yqg5b6u5L+h77yaMjU2ODg4NTEzNSZuYnNwOyZuYnNw
            OyDku47ov5npu5HoibLnmoTmraPmlrnlvaLkuK0=
            ----boundary_3658080_51a0ee0b-d096-4c14-bb0c-c0b4f7d69726
            Content-Type: text/html; charset=utf-8
            Content-Transfer-Encoding: base64

            5pyJ5q2j6KeE5Y+R56Wo5Y+v5Lul5byA77yM5Lu35qC85LyY5oOg77yM6ZW/5pyf
            5pyJ5pWI77yM6ZyA6KaB5Yqg5b6u5L+h77yaMjU2ODg4NTEzNSZuYnNwOyZuYnNw
            OyDku47ov5npu5HoibLnmoTmraPmlrnlvaLkuK0=
            ----boundary_3658080_51a0ee0b-d096-4c14-bb0c-c0b4f7d69726--


            --------------Boundary-00=_182E1KSR955BHUC3LVC0--

          """

def mocked_get_file_from_s3_inbound_message(bucket_key, bucket_name, bucket_region):
  return """
            Return-Path: <inboundemail@gmail.com>
            Received: from mail-il1-f173.google.com (mail-il1-f173.google.com [209.85.166.173])
            by inbound-smtp.us-east-1.amazonaws.com with SMTP id go5h9lga6venksb3hii7cjr7ci2ss9c2ponrr0o1
            for myemail@sesdomain.com;
            Tue, 02 Feb 2021 20:25:59 +0000 (UTC)
            X-SES-Spam-Verdict: PASS
            X-SES-Virus-Verdict: PASS
            Received-SPF: pass (spfCheck: domain of _spf.google.com designates 209.85.166.173 as permitted sender) client-ip=209.85.166.173; envelope-from=inboundemail@gmail.com; helo=mail-il1-f173.google.com;
            Authentication-Results: amazonses.com;
            spf=pass (spfCheck: domain of _spf.google.com designates 209.85.166.173 as permitted sender) client-ip=209.85.166.173; envelope-from=inboundemail@gmail.com; helo=mail-il1-f173.google.com;
            dkim=pass header.i=@gmail.com;
            dmarc=pass header.from=gmail.com;
            X-SES-RECEIPT: AEFBQUFBQUFBQUFFbVJVcmZhdlZKQ1hBVlBvVHpaRVhISmtnZ2ZoZ1BXMGltTmZsUGVlTm85b0toaC9XNUNWKzQ4OUVwL0J3OGxOSDl1VXB5MzFZak9PY2VvMTN2eVB0TUNYcWhqemFBWktSVDBrK3NsWXV0VDltY1BYcGlZYnpmMWpWcG1hUkVUemtlMER2cERlb1pxaWIzU25VQkZFNWx4RDRLNzVoTkxvS2p3RXZLZmJRZklvNFh6TWkwTFk3YUNEbzBzSlNweHMybW9NcUZBWVJFaTI5L255bVB6ekNyckFkMWdUcjhPTTRyWnVkUVozSUlSMmFPYWN1d0RvQUMxMTI3bkR3emdaTXdaVzk0c1AxV2hlKzFrU2hZc01UMi9NcGF2RzdGUGc3SVhyKzdKNXdyWHc9PQ==
            X-SES-DKIM-SIGNATURE: a=rsa-sha256; q=dns/txt; b=Xxa3Ugz7Wb3KjMiD/IzjJ10UVZh0WskkyxGn4FTNOOKs8s3PiJuO/0esfUpqq/SFqVtnAVZdHFh00kzObV2yfbr+fX++VDf+N6r6VcBsn0gWdFbXItfg4g2IzMYKcK7eTUpASyK14iC5Gn4k50SJsUdILOk6syqEhKbOizT9lgc=; c=relaxed/simple; s=224i4yxa5dv7c2xz3womw6peuasteono; d=amazonses.com; t=1612297559; v=1; bh=aknS6ehekWSprKyMsZIlv/4wEOpumQJe3lxJUDTMf2c=; h=From:To:Cc:Bcc:Subject:Date:Message-ID:MIME-Version:Content-Type:X-SES-RECEIPT;
            Received: by mail-il1-f173.google.com with SMTP id z18so20077256ile.9
                    for <myemail@sesdomain.com>; Tue, 02 Feb 2021 12:25:59 -0800 (PST)
            DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
                    d=gmail.com; s=20161025;
                    h=mime-version:from:date:message-id:subject:to;
                    bh=aknS6ehekWSprKyMsZIlv/4wEOpumQJe3lxJUDTMf2c=;
                    b=Jacj+vgZUY9lDDbHo1O/LI/ztGsSJyhjuR6oG537IO6rASEUFQMtSzPcyihvgwpgmm
                    ++KS3LwAAmID2XohtCY5DHlZ9/VexmIBPNxh0CMMISdUzYjmADZkDNsB5T2GUh5aGSLe
                    Bf/BCSuRZV9PXeg+nD91cfeDB9jK7Vvf+OWAC1TPcRwNqnj87mP38HuojUg40l94jjRm
                    RT6zL/UQCTi0qG7Jz55PmRbzyW0g9es519Kk4oTvRUgSe9xKi4NTLEIlqUPTSGlFA9Bf
                    e6tNjawQQ4HsbQcuZIGXAB/FOyAVfKn997kvxBwJgxcTVF/2ehSX0PeWj4lWkl4uAOGQ
                    VioA==
            X-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
                    d=1e100.net; s=20161025;
                    h=x-gm-message-state:mime-version:from:date:message-id:subject:to;
                    bh=aknS6ehekWSprKyMsZIlv/4wEOpumQJe3lxJUDTMf2c=;
                    b=RGhJ4oe7PCx3RoNDNT/2WGaRxlkHR8QZCdksSZGckeHneT8MivnfSd380gzY2y8D2i
                    Lgcxbr6e/DZMxYGdecJNswvmWtuGd4rtXn89lX/p3JKRwtuOkcX7drnd/btr3MVSZz3Y
                    i7T3EXGg2HyIuYnqsiZVEmc2LKc31xtXQNilbRnwzz0oC7RmFKFtaf93lO2FXHDwRr1j
                    ZCUu2dMYiEKVlzmda9pQueiLsu1uj2P+J4nHKXBCPAhogbQTpLSscLsR844BbNx/Tg0d
                    9/Qs8MrEOFC+j3TujGl9euWxD0eWuQQ0RWQ63W1eEbm7UY3WJDaTlMGJvGACJ4iN/JF3
                    ckEg==
            X-Gm-Message-State: AOAM533C8BjDo33mh+sdoacXrUA7SpcVvqYCv3SpigMBGQWD+KTNxGwH
              4a9SchGRRCBrFh9BK+8chTouNnAKBFIxwqpDFmo5yeVKkqI9
            X-Google-Smtp-Source: ABdhPJwcchZaCznGW1xgzE55+aW83B+dnsghEiPjtSBiybnbXqlPXiWFMX6R0bDq0SJQLFbZ2YENM04DYhuOshEdnGI=
            X-Received: by 2002:a92:c265:: with SMTP id h5mr18420264ild.225.1612297558385;
            Tue, 02 Feb 2021 12:25:58 -0800 (PST)
            MIME-Version: 1.0
            From: Inbound Email <inboundemail@gmail.com>
            Date: Tue, 2 Feb 2021 20:25:47 +0000
            Message-ID: <CAC87shyJzGbPsSGDiJtG-0cR8XUSqjTG3W=YzCydV4i_vhx=nw@mail.gmail.com>
            Subject: Hello!
            To: My SES Domain Email myemail@sesdomain.com
            Content-Type: multipart/alternative; boundary="0000000000003d6a7805ba60473f"

            --0000000000003d6a7805ba60473f
            Content-Type: text/plain; charset="UTF-8"

            Hello! Inbound email message here.

            --0000000000003d6a7805ba60473f
            Content-Type: text/html; charset="UTF-8"

            <div dir="ltr">Hello!</div>

            --0000000000003d6a7805ba60473f--
          """

def mocked_get_file_from_s3_uncategorized(bucket_key, bucket_name, bucket_region):
  return "Just a string, cannot be categorized."

def mocked_send_email_through_ses(content_type, notification_email_content):
  return 

def mocked_send_email_through_ses_error(content_type, notification_email_content):
  raise Exception('ses email failed to send')

class ParseEmailTest(unittest.TestCase):

  @mock.patch('parse_email_and_notify.app.send_notification_email', side_effect=mocked_send_email_through_ses)
  @mock.patch('parse_email_and_notify.app.get_file', side_effect=mocked_get_file_from_s3_delivery_failure)
  def test_delivery_failure(self, s3_get_file_mock, send_email_ses_mock):

    response = lambda_handler(self.get_sns_event(), "")

    self.assertEqual(s3_get_file_mock.call_count, 1)
    self.assertEqual(send_email_ses_mock.call_count, 1)
    self.assertEqual('delivery failure (bad email)', send_email_ses_mock.call_args[0][0])
    self.assertEqual('Message send success.', response)

  @mock.patch('parse_email_and_notify.app.send_notification_email', side_effect=mocked_send_email_through_ses)
  @mock.patch('parse_email_and_notify.app.get_file', side_effect=mocked_get_file_from_s3_delivery_error)
  def test_delivery_error(self, s3_get_file_mock, send_email_ses_mock):

    response = lambda_handler(self.get_sns_event(), "")

    self.assertEqual(s3_get_file_mock.call_count, 1)
    self.assertEqual(send_email_ses_mock.call_count, 1)
    self.assertEqual('delivery error (bot)', send_email_ses_mock.call_args[0][0])
    self.assertEqual('Message send success.', response)
  
  @mock.patch('parse_email_and_notify.app.send_notification_email', side_effect=mocked_send_email_through_ses)
  @mock.patch('parse_email_and_notify.app.get_file', side_effect=mocked_get_file_from_s3_inbound_message)
  def test_inbound_message(self, s3_get_file_mock, send_email_ses_mock):

    response = lambda_handler(self.get_sns_event(), "")

    self.assertEqual(s3_get_file_mock.call_count, 1)
    self.assertEqual(send_email_ses_mock.call_count, 1)
    self.assertEqual('inbound message', send_email_ses_mock.call_args[0][0])
    self.assertEqual('Message send success.', response)

  @mock.patch('parse_email_and_notify.app.send_notification_email', side_effect=mocked_send_email_through_ses)
  @mock.patch('parse_email_and_notify.app.get_file', side_effect=mocked_get_file_from_s3_uncategorized)
  def test_uncategorized_type(self, s3_get_file_mock, send_email_ses_mock):

    response = lambda_handler(self.get_sns_event(), "")

    self.assertEqual(s3_get_file_mock.call_count, 1)
    self.assertEqual(send_email_ses_mock.call_count, 1)
    self.assertEqual('uncategorized email type', send_email_ses_mock.call_args[0][0])
    self.assertEqual('Message send success.', response)

  @mock.patch('parse_email_and_notify.app.send_notification_email', side_effect=mocked_send_email_through_ses_error)
  @mock.patch('parse_email_and_notify.app.get_file', side_effect=mocked_get_file_from_s3_delivery_failure)
  def test_ses_send_error(self, s3_get_file_mock, send_email_ses_error_mock):

    response = lambda_handler(self.get_sns_event(), "")

    self.assertEqual(s3_get_file_mock.call_count, 1)
    self.assertEqual(send_email_ses_error_mock.call_count, 1)
    self.assertEqual('delivery failure (bad email)', send_email_ses_error_mock.call_args[0][0])
    self.assertEqual('Message send failed, error: ses email failed to send', response)

  def get_sns_event(self):
    return {
      "Records": [
          {
            "eventVersion": "2.1",
            "eventSource": "aws:s3",
            "awsRegion": "us-east-1",
            "eventTime": "2020-06-13T19:53:35.254Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {
              "principalId": "AWS:12345"
            },
            "requestParameters": {
              "sourceIPAddress": "10.000.000.00"
            },
            "responseElements": {
              "x-amz-request-id": "F01D9C1267055212",
              "x-amz-id-2": "GYFWY8GgZOdenhoxN6SVx/3wCrwkNw/aNMeYaT7ryc4JyxWopi2wu2bQQSw555f9j2zcJ8HQ608jaD3ArEBVP8PWEjgj6hiQaa2"
            },
            "s3": {
              "s3SchemaVersion": "1.0",
              "configurationId": "087361b14-473b-4746-87495-5d1d9cc53115e",
              "bucket": {
                "name": "my-email-replies-bucket",
                "ownerIdentity": {
                  "principalId": "AWS:12345"
                },
                "arn": "arn:aws:s3:::my-email-replies-bucket"
              },
              "object": {
                "key": "message-key",
                "size": 3992,
                "eTag": "bf61672395dd1bf2a",
                "sequencer": "005EE52E"
              }
            }
          }
        ]
      }

if __name__ == '__main__':
  unittest.main()
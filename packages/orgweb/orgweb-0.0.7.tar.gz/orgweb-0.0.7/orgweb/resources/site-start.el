;; [[file:../../org/resources/site-start.org::*use-package][use-package:1]]
(require 'package)

(unless (package-installed-p 'use-package)
  (package-refresh-contents)
  (package-install 'use-package)
  (eval-when-compile
    (unless (bound-and-true-p package--initialized)
      (package-initialize))  ;; be sure load-path includes package directories
    (require 'use-package)))
;; use-package:1 ends here

;; [[file:../../org/resources/site-start.org::*Use Packages][Use Packages:1]]
(use-package org)
(use-package dockerfile-mode)
(use-package yaml-mode)
(use-package terraform-mode)
(use-package graphviz-dot-mode)
(use-package plantuml-mode)
(use-package toml-mode)
;; Use Packages:1 ends here

;; [[file:../../org/resources/site-start.org::*Configure PlantUML][Configure PlantUML:1]]
(setq plantuml-jar-path "/usr/bin/plantuml")
(setq org-plantuml-executable-path "/usr/bin/plantuml")
(setq plantuml-default-exec-mode 'executable)
(setq org-plantuml-exec-mode 'plantuml)
;; Configure PlantUML:1 ends here

;; [[file:../../org/resources/site-start.org::*Configure Org-babel][Configure Org-babel:1]]
(org-babel-do-load-languages
  'org-babel-load-languages
  '((emacs-lisp . t)
    (python . t)
    (dot . t)
    (plantuml . t)))
;; Configure Org-babel:1 ends here

;; [[file:../../org/resources/site-start.org::*Disable Backup Files][Disable Backup Files:1]]
(setq make-backup-files nil)
;; Disable Backup Files:1 ends here

;; [[file:../../org/resources/site-start.org::*Configure python-mode][Configure python-mode:1]]
(custom-set-variables
 '(indent-tabs-mode nil)
 '(python-indent-guess-indent-offset t)
 '(python-indent-guess-indent-offset-verbose nil)
 '(org-edit-src-content-indentation 0))
;; Configure python-mode:1 ends here

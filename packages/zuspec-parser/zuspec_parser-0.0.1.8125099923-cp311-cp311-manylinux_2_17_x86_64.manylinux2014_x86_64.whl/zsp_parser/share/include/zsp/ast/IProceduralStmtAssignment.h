/****************************************************************************
 * IProceduralStmtAssignment.h
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 ****************************************************************************/
#pragma once
#include <stdint.h>
#include <map>
#include <memory>
#include <set>
#include <string>
#include <vector>
#include "zsp/ast/impl/UP.h"
#include "zsp/ast/IVisitor.h"
#include "zsp/ast/IExecStmt.h"

#include "zsp/ast/AssignOp.h"
namespace zsp {
namespace ast {

class IExecStmt;
using IExecStmtUP=UP<IExecStmt>;
typedef std::shared_ptr<IExecStmt> IExecStmtSP;
class IExpr;
using IExprUP=UP<IExpr>;
typedef std::shared_ptr<IExpr> IExprSP;
class IProceduralStmtAssignment;
using IProceduralStmtAssignmentUP=UP<IProceduralStmtAssignment>;
class IProceduralStmtAssignment : public virtual IExecStmt {
public:
    
    virtual ~IProceduralStmtAssignment() { }
    
    
    virtual IExpr *getLhs() const = 0;
    
    virtual void setLhs(IExpr *v, bool own=true) = 0;
    
    virtual AssignOp getOp() const = 0;
    
    virtual void setOp(AssignOp v) = 0;
    
    virtual IExpr *getRhs() const = 0;
    
    virtual void setRhs(IExpr *v, bool own=true) = 0;
};
    
    } // namespace zsp
    } // namespace ast
    
